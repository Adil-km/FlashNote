import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Check if homepage loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_about(client):
    """Check if about page returns 200 or 404 depending on README.md"""
    response = client.get('/about')
    assert response.status_code in (200, 404)

def test_check_status(client):
    """Check if status route returns JSON"""
    response = client.get('/check_status')
    assert response.status_code == 200
    data = response.get_json()
    assert "ready" in data
