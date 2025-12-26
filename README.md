```md
# ☕ Coffee Recipes  
*Share, discover, and savour the perfect cup.*

![Flask](https://img.shields.io/badge/Flask-2.3+-black?logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A clean, full-stack Flask application for managing coffee recipes — built with RESTful principles, user auth, and modern frontend ergonomics. Perfect for learning, demos, or extending into a real-world app.

---

## Features

- **User accounts** — register, log in, manage your profile  
- **Full CRUD** — create, view, edit, and delete coffee recipes  
- **Rich media** — upload local images or link to external URLs  
- **Smart organization** — tag recipes and filter by tag or keyword  
- **Engagement** — like and save your favourite brews  
- **API-first** — complete REST API with auto-generated docs (Swagger)  
- **Tested** — 100% passing `pytest` suite  
- **Production-ready** — structured for easy deployment (VPS, Render, Docker)

---

## Quick Start (Local Development)

```powershell
# 1. Clone & enter project
git clone https://github.com/yourname/coffee-recipes.git
cd coffee-recipes

# 2. Set up virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows (PowerShell)
# source .venv/bin/activate           # Linux/macOS

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

Visit:  
- **Web UI**: [http://127.0.0.1:5000](http://127.0.0.1:5000)  
- **API Docs**: [http://127.0.0.1:5000/apidocs](http://127.0.0.1:5000/apidocs)

---

## Testing

Ensure everything works as expected:

```bash
pytest -v
```

All tests should pass. Warnings about `Query.get()` are safe to ignore (SQLAlchemy 1.x → 2.0 deprecation).

---

## Project Structure

```
coffee-recipes/
├── app/                   # Core application
│   ├── __init__.py        # App factory
│   ├── models.py          # SQLAlchemy models
│   ├── routes_api.py      # REST API (JSON)
│   ├── routes_web.py      # HTML views
│   ├── auth.py            # Login/registration
│   ├── forms.py           # WTForms validation
│   ├── templates/         # Jinja2 templates
│   └── static/            # CSS, JS, uploads
├── migrations/            # DB schema history (Flask-Migrate)
├── scripts/
│   └── seed_recipes.py    # Add sample data
├── tests/                 # pytest suite
├── run.py                 # Entry point
├── swagger.yml            # OpenAPI spec
├── requirements.txt
└── README.md
```

---

## Seed Sample Data

Add realistic demo recipes (with Unsplash images):

```bash
python scripts/seed_recipes.py
```

Great for screenshots, demos, or testing UI flows.

---

## Tech Stack

- **Backend**: Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy  
- **ORM**: SQLAlchemy (with SQLite in dev, PostgreSQL-ready)  
- **API Docs**: Flasgger (OpenAPI 3.0)  
- **Frontend**: Bootstrap 5, Jinja2, vanilla JS  
- **Testing**: pytest, Flask test client  
- **DB Migrations**: Flask-Migrate (Alembic)