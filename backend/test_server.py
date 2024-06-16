import pytest
import sys
import os
import psycopg2
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from server import app  
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Hello world!"

def test_health_route(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'msg': 'OK'}

def test_get_users(client):
    with patch('repo.db.postgresDB.execute_stmt') as mock_execute:
        mock_execute.return_value = [('user1',), ('user2',)]
        response = client.get('/get_users')
        assert response.status_code == 200
        assert response.json == [['user1'], ['user2']]

def test_transaction_route(client):
    with patch('repo.db.postgresDB.execute_stmt') as mock_execute:
        mock_execute.return_value = [(1, '支出', '食', 500, 2024, 9, 24)]
        response = client.get('/api/transaction?year=2024&month=9&day=24&id=1')
        assert response.status_code == 200

def test_balance_month(client):
    with patch('repo.db.postgresDB.execute_stmt') as mock_execute:
        '''mock_execute.side_effect = Exception('Database error')
        response = client.get('/api/balance/month?year=2024&month=9&id=1')
        assert response.status_code == 500
        assert response.json == {'error': 'Data fetch failed'}'''
        
        mock_execute.side_effect = None
        mock_execute.return_value = [(1, '支出', '食', 500, 2024, 9, 24)]
        response = client.get('/api/balance/month?year=2024&month=9&id=1')
        assert response.status_code == 200
        assert response.json == {'month balance': 0}

'''def test_database_connection_retry():
    with patch('psycopg2.connect', side_effect=[psycopg2.Error("Connection failed"), None]) as mock_db:
        response = None
        try:
            app.run()
            response = 'Connected'
        except Exception as e:
            response = str(e)
        assert mock_db.call_count == 2
        assert response != 'Connection failed' '''