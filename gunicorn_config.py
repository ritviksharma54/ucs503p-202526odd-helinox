# Gunicorn configuration file
import os

# Bind to the port provided by Render
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"

# Worker configuration
workers = 2  # Number of worker processes
worker_class = "sync"  # Use sync workers (can handle long requests)
timeout = 180  # 3 minutes timeout for AI processing (increased from default 30s)
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Graceful timeout for shutdown
graceful_timeout = 30
