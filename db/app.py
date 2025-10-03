"""Database service for the multitier application."""
from flask import Flask
import numpy as np

DATA_LENGTH = 200

app = Flask(__name__)

# ----------------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------------
@app.route('/airquality', methods=['GET'])
def airquality():
    """Simulate a database query returning real-time air quality data."""
    return np.random.rand(DATA_LENGTH).tolist(), 200
