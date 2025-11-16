# AIRecipeFinder

AIRecipeFinder — Django + Tailwind project that generates recipes using Groq Llama-3 (optionally) and fetches related YouTube tutorials (optionally). The project ships with mock fallbacks so the UI is fully usable without API keys during development.

Table of contents
- Project summary
- Features
- Quickstart (development)
- Environment variables
- Running the app
- Building assets (Tailwind)
- Admin and authentication
- Project structure
- Services (Groq + YouTube)
- Notes on deployment
- Contributing

Project summary
---------------
This repository contains a Django project `AIRecipeFinder` and an app `recipes` that provides:

- A modern, responsive UI (Tailwind CSS) for entering ingredients and receiving AI-generated recipes.
- A recipe detail view with ingredients, numbered steps, and related YouTube tutorial cards.
- Authentication (signup/login/logout) and a dashboard showing user stats and simple analytics (Chart.js).
- Services for calling Groq Llama-3 and the YouTube Data API; both services return safe mock data when API keys are not configured, so you can develop without external keys.

Features
--------
- AI Recipe generation (Groq Llama-3) — optional: controlled by `GROQ_API_KEY`.
- YouTube video search for tutorials — optional: controlled by `YOUTUBE_API_KEY`.
- Tailwind CSS-based UI with soft-mint theme and rounded cards.
- User registration, login, dashboard, and saved recipes models.
- Minimal services implementation in `recipes/services/` with robust fallbacks.

Quickstart (development)
------------------------
Prerequisites:
- Python 3.11+ (3.13 tested in this environment)
- Node.js + npm

Open PowerShell and run:

```powershell
cd C:\Users\kunda\OneDrive\Desktop\ai_recipe_suggestions
# Create & activate virtualenv
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Install JS dev dependencies and build Tailwind once
npm install
npm run build:css

# Create .env from .env.example and fill keys if you have them
copy .env.example .env
notepad .env  # edit to add real keys if available

# Run database migrations and collect static files (for dev we use collectstatic to serve staticfiles folder)
python manage.py migrate
python manage.py collectstatic --noinput

# Create an admin user (interactive)
python manage.py createsuperuser

# Start development server
python manage.py runserver 127.0.0.1:8000

# Visit: http://127.0.0.1:8000/
```

Environment variables
---------------------
Create a `.env` file in the project root (we include `.env.example`). Important keys:

- `SECRET_KEY` — Django secret
- `DEBUG` — `True` for local dev
- `DATABASE_URL` — e.g. `sqlite:///db.sqlite3` (default) or a Postgres URL
- `GROQ_API_KEY` — (optional) API key for Groq Llama-3
- `GROQ_API_URL` — (optional) Groq API endpoint (default set in `.env.example`)
- `YOUTUBE_API_KEY` — (optional) Google YouTube Data API key
- `ALLOWED_HOSTS` — comma-separated hosts

If `GROQ_API_KEY` or `YOUTUBE_API_KEY` are not set the services will return deterministic mock content so you can test the UI.

Running the app
---------------
- After running `python manage.py runserver` the site is available at `http://127.0.0.1:8000/`.
- The admin is at `/admin/` (create a superuser to access it).
- If you try to access `/dashboard/` while unauthenticated you will be redirected to the login page with `?next=/dashboard/` and returned after successful login.

Building assets (Tailwind)
-------------------------
- Edit `assets/input.css` and then run:

```powershell
npm run build:css
```

- For development live rebuilds:

```powershell
npm run watch:css
```

Project structure (important files)
----------------------------------
- `AIRecipeFinder/` — Django project settings and WSGI
- `recipes/` — main app
	- `models.py` — `Recipe`, `SearchHistory`, `SavedRecipe`
	- `views.py` — class-based views: `HomeView`, `RecipeDetailView`, `DashboardView`, `RegisterView`, `LoginView`
	- `services/` — `groq_ai.py`, `youtube.py` (contains mock fallbacks)
	- `templates/recipes/` — templates for home, recipe detail, dashboard, login, register
	- `static/recipes/` — compiled CSS and JS (Chart.js) assets
- `assets/input.css` — Tailwind entry CSS
- `tailwind.config.js`, `postcss.config.js`, `package.json` — Tailwind build
- `.env.example` — example environment variables

Services (Groq + YouTube)
-------------------------
- `recipes/services/groq_ai.py` — function `generate_recipe(ingredients: str)`:
	- If `GROQ_API_KEY` set, attempts to call Groq API and parse JSON; falls back safely on network/parse errors.
	- If `GROQ_API_KEY` is not set, returns a deterministic mock recipe derived from the ingredients.

- `recipes/services/youtube.py` — function `search_videos(query: str)`:
	- If `YOUTUBE_API_KEY` set, calls YouTube Data API and returns top results.
	- If not set or API call fails, returns three mock video entries with placeholder thumbnails.

This design lets you iterate the UI and flows without external API credentials during development.

Dashboard and authentication
----------------------------
- Login/Signup are implemented using Django auth and class-based views.
- The `LoginView` respects a `next` parameter to redirect users after login.
- `DashboardView` is protected with `LoginRequiredMixin` and shows counts and a Chart.js doughnut chart for difficulty distribution.

Notes on deployment
-------------------
- For production set `DEBUG=False`, configure `ALLOWED_HOSTS`, and use a production-ready DB (Postgres) via `DATABASE_URL`.
- Use a WSGI/ASGI server (Gunicorn + Nginx or Daphne + Nginx) and serve static files from a CDN or S3.
- Keep `SECRET_KEY` secret and rotate periodically.

Contributing
------------
- If you'd like help improving UI, adding real Groq integration with better prompts, or implementing saved/unsaved recipe flows, open an issue or submit a PR.
- Tests: add unit tests under `recipes/tests.py` and run with `python manage.py test`.

License
-------
This project scaffold is provided for development and learning. Add a license file if you plan to publish or share it.
