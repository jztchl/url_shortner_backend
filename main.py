from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db import SessionLocal, ShortUrls
from cache import set_url, get_url
from pydantic import BaseModel, HttpUrl
import hashlib, string
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
class URLRequest(BaseModel):
    original_url: HttpUrl
     
app = FastAPI(title="URL Shortener")
ALLOWED_ORIGINS=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
BASE_URL=os.getenv("BASE_URL", "http://localhost:9000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


BASE62 = string.digits + string.ascii_letters

def base62_encode(num: int) -> str:
    chars = []
    base = len(BASE62)
    while num > 0:
        num, rem = divmod(num, base)
        chars.append(BASE62[rem])
    return ''.join(reversed(chars)) or "0"

def hash_url(url: str, length: int = 8) -> str:
    hash_val = int(hashlib.sha256(url.encode()).hexdigest(), 16)
    short_code = base62_encode(hash_val)
    return short_code[:length]     

   
@app.post("/shorten")
def shorten_url(request: URLRequest, db: Session = Depends(get_db)):
    code = hash_url(str(request.original_url))
    if db.query(ShortUrls).filter(ShortUrls.short_code == code).first():
         set_url(code, str(request.original_url))
         return {"short_url": f"{BASE_URL}/{code}"}
    url_entry = ShortUrls(original_url=str(request.original_url), short_code=code)
    db.add(url_entry)
    db.commit()
    db.refresh(url_entry)
    set_url(code, str(request.original_url))

    return {"short_url": f"{BASE_URL}/{code}"}

@app.get("/{code}")
def redirect_to_url(code: str, db: Session = Depends(get_db)):
    original_url = get_url(code)
    if not original_url:
        url_entry = db.query(ShortUrls).filter(ShortUrls.short_code == code).first()
        if not url_entry:
            raise HTTPException(status_code=404, detail="URL not found")
        original_url = url_entry.original_url
        set_url(code, original_url)  


    return RedirectResponse(original_url)

