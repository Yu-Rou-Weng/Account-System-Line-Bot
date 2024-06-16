import http from 'k6/http';
import { check, group, sleep } from 'k6';

export let options = {
    vus: 5,
    duration: '1m',
    thresholds: {
        'http_req_duration': ['p(95)<500'], 
    }
};

function transaction_test() {
    group('API Transaction Endpoint', function () {
        var transactionUrl = 'http://localhost:5000/api/transaction?username=TestUser&year=2024&month=9&day=24';
        var transactionResponse = http.get(transactionUrl);
        check(transactionResponse, {
            'transaction status is 200': (r) => r.status === 200
        });
    });
    sleep(1);
}

function balance_test() {
    group('API Balance Endpoint', function () {
        var balanceUrl = 'http://localhost:5000/api/balance/month?username=TestUser&year=2024&month=9';
        var balanceResponse = http.get(balanceUrl);
        check(balanceResponse, {
            'balance status is 200': (r) => r.status === 200
        });
    });
    sleep(1); 
}
function route_test() {
    group('API Route Endpoint', function () {
        var Url = 'http://localhost:5000/;
        var Response = http.get(Url);
        check(Response, {
            'status is 200': (r) => r.status === 200
        });
    });
    sleep(1); 
}
function getusers_test() {
    group('API Getusers Endpoint', function () {
        var Url = 'http://localhost:5000/get_users;
        var Response = http.get(Url);
        check(Response, {
            'status is 200': (r) => r.status === 200
        });
    });
    sleep(1); 
}
function testroute_test() {
group('API Test Endpoint', function () {
        var Url = 'http://localhost:5000/test;
        var Response = http.get(Url);
        check(Response, {
            'status is 200': (r) => r.status === 200
        });
    });
    sleep(1); 
}

export default function () {
    transaction_test();
    balance_test();
    route_test();
    getusers_test();
    testroute_test();
}
