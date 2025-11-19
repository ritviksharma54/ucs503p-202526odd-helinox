# Render Deployment Guide

## Architecture Decision

You have **two deployment options** for Render.com:

### Option 1: Separate Services (Recommended for Scale)
Deploy backend and frontend as separate services:
- **Backend**: Web Service (Python)
- **Frontend**: Static Site (or Web Service with Node)

### Option 2: Backend Serves Frontend (Simpler, Current Setup)
Flask serves the built Vue.js app as static files.

---

## Current Deployment (Option 2 - Simplest)

Since you're already deployed on Render, this is the **easiest migration path**:

### Steps:

1. **Build the frontend locally:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **The build creates `frontend/dist/` folder**

3. **Update Flask to serve the frontend:**
   - Flask will serve `frontend/dist/index.html` as the entry point
   - API routes remain at `/api/*`

4. **On Render.com:**
   - Keep your existing Web Service
   - Add build command:
     ```bash
     cd frontend && npm install && npm run build && cd .. && pip install -r requirements.txt
     ```
   - Start command remains:
     ```bash
     gunicorn -c gunicorn_config.py app:app
     ```
   - Set environment variable: `GOOGLE_API_KEY`

5. **Update `app/__init__.py` to serve frontend:**
   
   Add this to your `create_app()` function:
   ```python
   import os
   from flask import send_from_directory
   
   # Serve Vue.js frontend
   frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
   
   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve_frontend(path):
       if path and os.path.exists(os.path.join(frontend_dist, path)):
           return send_from_directory(frontend_dist, path)
       return send_from_directory(frontend_dist, 'index.html')
   ```

---

## Alternative: Separate Services (Option 1)

If you want to deploy frontend and backend separately:

### Backend (Web Service):
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn -c gunicorn_config.py app:app`
- **Environment Variables:** `GOOGLE_API_KEY`, `PORT=5000`

### Frontend (Static Site):
- **Build Command:** `cd frontend && npm install && npm run build`
- **Publish Directory:** `frontend/dist`
- **Rewrite Rules:** 
  - Source: `/*`
  - Destination: `/index.html` (for Vue Router)

### Update Frontend API URL:
Create `frontend/.env.production`:
```
VITE_API_URL=https://your-backend-service.onrender.com
```

Update Axios calls to use:
```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
axios.post(`${API_URL}/api/analyze`, ...)
```

---

## Recommendation for Your Case

Since you're **already deployed on Render**, I recommend **Option 2** (Backend serves Frontend):

✅ **Simplest migration** - no architecture changes  
✅ **Single service** - easier to manage  
✅ **No CORS issues** - same origin  
✅ **Lower cost** - one service instead of two  

Just need to:
1. Build frontend locally
2. Update Flask to serve `frontend/dist/`
3. Update Render build command to include frontend build
4. Push to GitHub and redeploy

Let me know which option you prefer and I'll help you configure it! 🚀
