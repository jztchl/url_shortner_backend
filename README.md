<p align="center">
  <img src="logo.webp" alt="app  Logo" width="200" >
</p>

# URL Shortener Backend (FastAPI + Postgres + Redis)

A **high-performance URL shortener backend** built with **FastAPI**, using **PostgreSQL** for persistent storage and **Redis** for caching frequently accessed URLs.
Runs entirely on the **`uv` package manager** ecosystem.

---

## 🚀 Features

* Shorten any valid URL
* Input validation with **Pydantic (`HttpUrl`)**
* Persistent storage with **PostgreSQL**
* High-speed caching with **Redis**
* CORS support (restricts frontend access)
* JSON API responses for easy consumption by frontend
* Production-ready architecture

---

## 💻 Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **Cache:** Redis
* **Validation:** Pydantic
* **Server:** Uvicorn 


---

## ⚡ Installation & Setup (using `uv`)

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/url-shortener-backend.git
cd url-shortener-backend
```

2. **Create and activate virtual environment**

```bash
uv venv create venv
uv venv activate venv
```

3. **Install dependencies from lockfile**

```bash
uv install
```

> `uv` will automatically read `uv.lock` and install the exact pinned versions.
4. **🛠 Postgres & Redis Setup**

* Make sure you have **PostgreSQL** running and a database ready for the URL shortener.
* Make sure you have **Redis** running for caching.


5. **Configure environment variables**

Create a `.env` file in the root directory:

```env
ALLOWED_ORIGINS=https://url-shortner-jztchl.vercel.app,http://localhost:5173
BASE_URL=http://localhost:8000
DATABASE_URL=postgresql://your_db_user:your_db_password@localhost:5432/url_shortener
REDIS_URL=redis://localhost:6379
```

## 🚀 Running the Backend

```bash
uvicorn main:app --reload
```

## 🔗 API Endpoint

**POST /shorten**

* **Request Body:**

```json
{
  "original_url": "https://www.example.com"
}
```

* **Response:**

```json
{
  "short_url": "http://localhost:8000/abc123"
}
```

> Make sure to include `http://` or `https://` in the URL for validation.

---

## 🔧 Folder Structure

```
backend/
├─ main.py           # FastAPI app
├─ models.py         # Pydantic models
├─ database.py       # PostgreSQL connection & ORM logic
├─ cache.py          # Redis caching logic
├─ uv.lock           # Dependencies lockfile for uv
├─ .env
└─ README.md
```

---

## 📜 License

This project is **MIT Licensed**.
