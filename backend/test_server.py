import pytest
from server import app, get_id  
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
    mock_users = [
        {'id': 1, 'username': 'user1'}
    ]
    with patch('server.db.execute_stmt', return_value=mock_users) as mock_execute:
        response = client.get('/get_users')
        assert response.status_code == 200
        returned_ids = [user['id'] for user in response.json]
        expected_ids = [1]
        assert returned_ids == expected_ids

def test_get_transaction_found(client):
    with patch('server.db.execute_stmt', return_value=[(1, '支出', '食', 500, '備註', 2024, 9, 24)]) as mock_execute:
        response = client.get('/api/transaction?year=2024&month=9&day=24&id=1')
        assert response.status_code == 200
        assert '2024年9月24日' in response.json['records']

def test_get_transaction_not_found(client):
    with patch('server.db.execute_stmt', return_value=[]) as mock_execute:
        response = client.get('/api/transaction?year=2024&month=9&day=24&id=1')
        assert response.status_code == 404

def test_post_transaction_success(client):
    with patch('server.db.execute_stmt', return_value=[(1, )]) as mock_execute:  
        response = client.post('/api/transaction?id=1&iotype=支出&consume_type=食&amount=500&time_year=2024&time_month=9&time_date=24&remark=備註')
        assert response.status_code == 200


def test_balance_month_with_records(client):
    with patch('server.db.execute_stmt', return_value=[('收入', 500), ('支出', 300)]) as mock_execute:
        response = client.get('/api/balance/month?year=2024&month=9&id=1')
        assert response.status_code == 200
        assert response.json['month balance'] == 200

def test_balance_month_no_records(client):
    with patch('server.db.execute_stmt', return_value=[]) as mock_execute:
        response = client.get('/api/balance/month?year=2024&month=9&id=1')
        assert response.status_code == 404

def test_get_id_existing_user(client):
    with patch('server.db.execute_stmt', return_value=[(1, 'user1')]) as mock_execute:
        assert get_id('user1') == 1

def test_get_id_new_user(client):
    with patch('server.db.execute_stmt', side_effect=[[], [(2, 'user2')]]) as mock_execute:
        assert get_id('user2') == 2

if __name__ == "__main__":
    pytest.main()
