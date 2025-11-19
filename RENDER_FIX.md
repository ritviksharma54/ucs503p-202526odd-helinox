# Quick Fix for Render Deployment

## The Problem
There was a naming conflict between `app.py` and the `app/` directory. Gunicorn was trying to import from the wrong one.

## The Solution
Created `wsgi.py` as the entry point and updated Gunicorn to use `wsgi:app`.

## Update Render Settings

**Change your Render Start Command to:**
```bash
gunicorn wsgi:app
```

Or if using the config file:
```bash
gunicorn -c gunicorn_config.py wsgi:app
```

## Push the Fix

```bash
git add wsgi.py gunicorn_config.py
git commit -m "Fix Gunicorn naming conflict with wsgi.py"
git push origin main
```

Render will automatically redeploy with the fix! 🚀
