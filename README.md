# stationary-finalcode  

A small Django‑based web application that showcases a simple inventory/point‑of‑sale system for stationery items. The repository contains the full source code, database migrations, sample images, and a brief project description document.

---  

## Overview  

`stationary-finalcode` demonstrates how to build a minimal yet functional CRUD interface for managing stationery products, sales, and purchases. It includes:

* A Django project (`myproject`) with a single app (`myapp`).  
* Database schema migrations covering items, sales, and purchase records.  
* Sample HTML templates and static images (e.g., `Itme_images/201_3.png`).  
* A Word document (`Project File.docx`) that outlines the original assignment requirements.  

The project is intended for educational purposes—perfect for newcomers who want to explore Django models, migrations, and basic view/template wiring.

---  

## Features  

| Feature | Description |
|---------|-------------|
| **Item catalog** | Store and display stationery items with images. |
| **Sales & purchases** | Record transactions via simple forms. |
| **Admin interface** | Full CRUD support through Django’s built‑in admin. |
| **Database migrations** | Incremental schema changes (`0001_initial` → `0004_remove_items_last_activity_and_more`). |
| **Static assets** | Sample PNG images located in `Itme_images/`. |
| **Test suite** | Basic unit tests in `myapp/tests.py`. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Django 4.x |
| **Database** | SQLite (default) – easy for local development |
| **Frontend** | HTML5, CSS (static files) |
| **Version control** | Git (GitHub) |
| **Packaging** | `manage.py` for Django management commands |

---  

## Installation  

> **Prerequisite:** Ensure Python 3.9+ and `git` are installed on your machine.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/stationary-finalcode.git
cd stationary-finalcode

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt   # If a requirements file is not present, run:
pip install Django==4.*           # Adjust version as needed

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser for the admin site
python manage.py createsuperuser
# Follow the prompts – use YOUR_OWN_EMAIL and a strong password.

# 6. Collect static files (optional for production)
python manage.py collectstatic
```

> **Note:** The repository does not ship a `requirements.txt`. The only required package is Django. Add any additional packages you use to a `requirements.txt` for reproducibility.

---  

## Usage  

```bash
# Start the development server
python manage.py runserver
```

Open your browser and navigate to:

* **Application:** `http://127.0.0.1:8000/` – the home page where items are listed.  
* **Admin panel:** `http://127.0.0.1:8000/admin/` – manage items, sales, and purchases.

### Common commands  

| Command | Purpose |
|---------|---------|
| `python manage.py makemigrations` | Create new migration files after model changes. |
| `python manage.py test` | Run the test suite (`myapp/tests.py`). |
| `python