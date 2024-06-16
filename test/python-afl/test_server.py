import pytest
from server import app, get_id, db
from repo.db import postgresDB
from unittest.mock import patch
import unittest
import random
import afl, os, sys, hack

def mockfunc(stmt_format, stmt_args, isSelect):
    raise Exception('foo')

def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route():
    client = client()
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode() == "Hello world!"

def test_health_route():
    client = client()
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'msg': 'OK'}

def test_get_transaction_found():
    client = client()
    inp = sys.stdin.read()
    a, b, c = inp.strip().split()
    a = int(a)
    b = int(b)
    c = int(c)
    with patch('server.db.execute_stmt', return_value=[(1, '支出', '食', 500, '備註', 2024, 9, 24)]) as mock_execute:
        response = client.get(f'/api/transaction?year={a}&month={b}&day={c}&id=1')

def test_get_transaction_not_found():
    client = client()
    inp = sys.stdin.read()
    a, b, c = inp.strip().split()
    a = int(a)
    b = int(b)
    c = int(c)
    with patch('server.db.execute_stmt', return_value=[]) as mock_execute:
        response = client.get(f'/api/transaction?year={a}&month={b}&day={c}&id=1')

def test_get_transaction_exception():
    client = client()
    inp = sys.stdin.read()
    a, b, c = inp.strip().split()
    a = int(a)
    b = int(b)
    c = int(c)
    with patch.object(postgresDB, 'execute_stmt', side_effect=mockfunc) as mock_execute:
        try:
            response = client.get(f'/api/transaction?year={a}&month={b}&day={c}&id=1')
        except Exception as e:
            assert e.__str__() == 'foo'

def test_post_transaction_success():
    client = client()
    inp = sys.stdin.read()
    a, b, c, d = inp.strip().split()
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    with patch('server.db.execute_stmt', return_value=[(1, )]) as mock_execute:  
        response = client.post(f'/api/transaction?id=1&iotype=支出&consume_type=食&amount={d}&time_year={a}&time_month={b}&time_date={c}&remark=備註')



def test_balance_month_with_records():
    client = client()
    inp = sys.stdin.read()
    a, b = inp.strip().split()
    a = int(a)
    b = int(b)
    with patch('server.db.execute_stmt', return_value=[('收入', 500), ('支出', 300)]) as mock_execute:
        response = client.get('/api/balance/month?year={a}}&month={b}&id=1')

def test_balance_month_no_records():
    client = client()
    inp = sys.stdin.read()
    a, b = inp.strip().split()
    a = int(a)
    b = int(b)
    with patch('server.db.execute_stmt', return_value=[]) as mock_execute:
        response = client.get('/api/balance/month?year=2024&month=9&id=1')

def test_balance_month_exception():
    client = client()
    inp = sys.stdin.read()
    a, b = inp.strip().split()
    a = int(a)
    b = int(b)
    with patch.object(postgresDB, 'execute_stmt', side_effect=mockfunc, return_value=[]) as mock_execute:
        try:
            response = client.get('/api/balance/month?year={a}&month={b}&id=1')
        except Exception as e:
            assert e.__str__() == 'foo'

def test_get_id_existing_user():
    client = client()
    with patch('server.db.execute_stmt', return_value=[(1, 'user1')]) as mock_execute:
        get_id('user1')

def test_get_id_new_user():
    client = client()
    with patch('server.db.execute_stmt', side_effect=[[], [(2, 'user2')]]) as mock_execute:
        get_id('user2')

if __name__ == "__main__":
    afl.init()
    sys.stdin.seek(0)

    random.seed(0)
    a = random.randint(1, 9)
    match a:
        case 1:
            test_home_route()
        case 2:
            test_health_route()
        case 3:
            test_get_transaction_found()
        case 4:
            test_get_transaction_not_found()
        case 5:
            test_get_transaction_exception()
        case 6:
            test_post_transaction_success()
        case 7:
            test_balance_month_with_records()
        case 8:
            test_balance_month_no_records()
        case 9:
            test_balance_month_exception()
    os._exit(0)
