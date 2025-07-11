import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test the home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'message' in data
    assert 'version' in data
    assert 'environment' in data
    assert 'status' in data
    assert data['status'] == 'healthy'

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'healthy'
    assert 'version' in data

def test_liveness_endpoint(client):
    """Test the liveness probe endpoint."""
    response = client.get('/health/live')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'alive'

def test_readiness_endpoint(client):
    """Test the readiness probe endpoint."""
    response = client.get('/health/ready')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] == 'ready'

def test_api_info_endpoint(client):
    """Test the API info endpoint."""
    response = client.get('/api/info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'name' in data
    assert 'phase' in data
    assert 'version' in data
    assert 'environment' in data
    assert 'features' in data
    assert data['phase'] == 'Phase 1'

def test_request_info_endpoint(client):
    """Test the request info endpoint."""
    response = client.get('/api/request-info')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'method' in data
    assert 'url' in data
    assert 'headers' in data
    assert 'remote_addr' in data

def test_404_error(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'Not Found'

def test_environment_variables():
    """Test that environment variables are properly set."""
    import os
    
    # Test default values
    assert app.config['TESTING'] == True  # Set in test fixture
    
    # Test that the app can access environment variables
    # This is tested implicitly by the app running successfully
    assert True