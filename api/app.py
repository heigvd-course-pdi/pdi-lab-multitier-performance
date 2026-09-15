"""Simple Flask API for a multitier application"""
import os
from flask import Flask, request
import requests
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

COMPUTE_URL = os.getenv('COMPUTE_URL')

# ----------------------------------------------------------------------------
# Prometheus metrics
# ----------------------------------------------------------------------------
# Gauges are used instead of a histogram to keep things simple.
AIRQUALITY_REQUEST_DURATION = Gauge('airquality_request_duration_seconds', 'Airquality request duration')

# ----------------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------------
@app.route('/airquality', methods=['GET'])
@AIRQUALITY_REQUEST_DURATION.time()
def airquality():
    """Generate a map with real-time air pollution data for a given country."""

    country = request.args.get('country')

    # Forward the request to the compute service
    response = requests.get(f'{COMPUTE_URL}?country={country}', timeout=5)
    if response.status_code != 200:
        return response.text, response.status_code

    # Send the image received from the compute service as response
    return response.content, 200, {'Content-Type': 'image/png'}

# ----------------------------------------------------------------------------
# Prometheus Metrics Endpoint
# ----------------------------------------------------------------------------
@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
