#!/usr/bin/env python3
"""
GCP Cloud Run Blueprint - Phase 1
Main Flask application with health checks and environment configuration
"""

import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configure for Cloud Run (behind proxy)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# Environment variables with defaults
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
VERSION = os.getenv('VERSION', '1.0.0')
PORT = int(os.getenv('PORT', 8080))

@app.route('/')
def home():
    """Main application endpoint"""
    return jsonify({
        'message': 'GCP Cloud Run Blueprint - Phase 1',
        'version': VERSION,
        'environment': ENVIRONMENT,
        'timestamp': datetime.utcnow().isoformat(),
        'status': 'healthy'
    })

@app.route('/health')
def health():
    """Health check endpoint for Cloud Run"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': VERSION
    })

@app.route('/health/live')
def liveness():
    """Liveness probe endpoint"""
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/health/ready')
def readiness():
    """Readiness probe endpoint"""
    return jsonify({
        'status': 'ready',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/info')
def api_info():
    """API information endpoint"""
    return jsonify({
        'name': 'GCP Cloud Run Blueprint',
        'phase': 'Phase 1',
        'version': VERSION,
        'environment': ENVIRONMENT,
        'features': [
            'Containerized web application',
            'Health check endpoints',
            'Environment variable configuration',
            'Auto-scaling configuration',
            'HTTPS enforcement',
            'Cloud Run service deployment'
        ]
    })

@app.route('/api/request-info')
def request_info():
    """Return request information for debugging"""
    return jsonify({
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers),
        'remote_addr': request.remote_addr,
        'user_agent': request.user_agent.string,
        'timestamp': datetime.utcnow().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'timestamp': datetime.utcnow().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'timestamp': datetime.utcnow().isoformat()
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting GCP Cloud Run Blueprint - Phase 1")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Version: {VERSION}")
    logger.info(f"Port: {PORT}")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=(ENVIRONMENT == 'development')
    )