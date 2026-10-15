"""
RescueVision AI - Production WSGI Entrypoint
Runs Waitress (production WSGI server for Windows/Linux) or gunicorn on Linux/Docker.

Usage:
    python wsgi.py
"""

import os
from waitress import serve
from app import app
from config import Config

if __name__ == "__main__":
    port = int(os.getenv("PORT", Config.PORT))
    host = os.getenv("HOST", "0.0.0.0")
    print("=" * 60)
    print("RescueVision AI - Production WSGI Server (Waitress)")
    print(f"Serving application on http://{host}:{port}")
    print("=" * 60)
    serve(app, host=host, port=port, threads=8)
