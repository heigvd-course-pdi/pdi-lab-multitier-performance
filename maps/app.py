"""Database service for the multitier application."""
import time
from flask import Flask

app = Flask(__name__)

# Read map from disk
with open('map.png', 'rb') as f:
    base_map = f.read()

# ----------------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------------
@app.route('/', methods=['GET'])
def airquality():
    """Simulate a slow external service."""
    time.sleep(0.02) # Simulate a slow external service
    return base_map, 200, {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=600'
    }
