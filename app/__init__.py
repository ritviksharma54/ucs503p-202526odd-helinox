import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app)
    
    # Import and register blueprints
    from app.routes.api import api_bp
    app.register_blueprint(api_bp)
    
    # Serve Vue.js frontend (for production)
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        # Serve API routes first (they have /api prefix)
        if path.startswith('api/'):
            return {'error': 'Not found'}, 404
            
        # Serve static files if they exist
        if path and os.path.exists(os.path.join(frontend_dist, path)):
            return send_from_directory(frontend_dist, path)
        
        # Otherwise serve index.html (for Vue Router)
        if os.path.exists(frontend_dist):
            return send_from_directory(frontend_dist, 'index.html')
        else:
            return {'message': 'Frontend not built. Run: cd frontend && npm run build'}, 200
    
    return app
