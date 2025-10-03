"""Compute service for the multi-tier application."""
import os
from flask import Flask, request
import requests
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
import numpy as np

app = Flask(__name__)

EXTERNAL_MAP_API = os.getenv('EXTERNAL_MAP_API_URL')
DATABASE_URL = os.getenv('DATABASE_URL')
SUPPORTED_COUNTRIES = {'switzerland', 'france', 'germany', 'italy', 'spain'}

# ----------------------------------------------------------------------------
# Prometheus metrics
# ----------------------------------------------------------------------------
# Gauges are used instead of a histogram to keep things simple.
EXTERNAL_API_DURATION = Gauge('external_api_duration_seconds', 'External API call duration')
DATABASE_DURATION = Gauge('database_query_duration_seconds', 'Database query duration')
COMPUTATION_DURATION = Gauge('computation_duration_seconds', 'Computation duration')
COMPUTE_REQUEST_DURATION = Gauge('total_compute_request_duration_seconds', 'Total compute request duration')

# ----------------------------------------------------------------------------
# API Endpoints
# ----------------------------------------------------------------------------
@app.route('/airquality', methods=['GET'])
@COMPUTE_REQUEST_DURATION.time()
def airquality():
    """Generate a map with real-time air pollution data for a given country."""

    country = request.args.get('country')
    if country not in SUPPORTED_COUNTRIES:
        return 'Unsupported country', 400

    # Get the map from the external map service
    with EXTERNAL_API_DURATION.time():
        response = requests.get(f'{EXTERNAL_MAP_API}?country={country}', timeout=5)
    if response.status_code != 200:
        return response.text, response.status_code
    base_map = response.content

    # Get real-time air quality data from the database
    with DATABASE_DURATION.time():
        response = requests.get(f'{DATABASE_URL}?country={country}', timeout=5)
        data = np.array(response.json())

    # Perform some computation on the data and the map
    with COMPUTATION_DURATION.time():
        map_with_data = compute_map(base_map, data)

    # Send the image received from the compute service as response
    return map_with_data, 200, {'Content-Type': 'image/png'}


# ----------------------------------------------------------------------------
# Computation function
# ----------------------------------------------------------------------------
def compute_map(base_map, data):
    """Simulate a complexe computation on the map and data."""
    _, _, _ = np.linalg.svd(np.outer(data, data))
    return base_map


# ----------------------------------------------------------------------------
# Prometheus Metrics Endpoint
# ----------------------------------------------------------------------------
@app.route('/metrics')
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
