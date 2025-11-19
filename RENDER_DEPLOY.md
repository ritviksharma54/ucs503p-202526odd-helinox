# Quick Deployment Guide for Render.com (Simplest Setup)

## What This Does
Flask serves the Vue.js app as static files. Everything runs from one service on Render.

## Steps to Deploy

### 1. Build Frontend Locally (One-time)
```bash
cd frontend
npm install
npm run build
```
This creates `frontend/dist/` folder with your Vue.js app.

### 2. Update Your Render.com Service

**Build Command:**
```bash
cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn -c gunicorn_config.py app:app
```

**Environment Variables:**
- `GOOGLE_API_KEY` = your_actual_google_gemini_api_key

### 3. Push to GitHub
```bash
git add .
git commit -m "Migrate to Vue.js frontend with dark mode"
git push origin main
```

Render will automatically detect changes and redeploy!

## That's It! 🚀

Your app will be live at: `https://your-service-name.onrender.com`

- Frontend: Served by Flask at `/`
- API: Available at `/api/analyze` and `/api/find_jobs`

## Troubleshooting

**If frontend doesn't show:**
```bash
# Rebuild frontend
cd frontend && npm run build

# Push again
git add frontend/dist
git commit -m "Update frontend build"
git push
```

**If API doesn't work:**
- Check `GOOGLE_API_KEY` is set in Render environment variables
- Check logs in Render dashboard
