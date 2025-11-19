# Quick Git Commit Guide

The commands are ready to execute. Please run these in your terminal:

```bash
# 1. Stage all changes
git add .

# 2. Commit with a meaningful message
git commit -m "Modernize to Vue.js 3 with dark mode and refactored Flask backend

- Refactored Flask backend into modular app/ structure
- Migrated frontend from templates to Vue.js 3 + Vite
- Implemented Obsidian & Teal dark mode theme
- Added missing features: text input, ZIP uploads
- Updated deployment configuration for Render.com
- Cleaned up legacy files and improved .gitignore
- Updated README and documentation"

# 3. Push to GitHub
git push origin main
```

Or if you prefer a shorter commit message:

```bash
git add .
git commit -m "Migrate to Vue.js 3 with dark mode and refactored Flask backend"
git push origin main
```

After pushing, Render.com will automatically detect the changes and redeploy your app! 🚀
