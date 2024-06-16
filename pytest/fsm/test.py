import sys
import sqlite3
import fsm
from pytest_mock import MockFixture
import pytest

class mockDBconn():
    def __init__(self):
        self.result = "default"
    def connect(self, str):
        return self
    def cursor(self):
        return self
    def commit(self):
        pass
    def execute(self, str):
        return self
    def fetchone(self):
        return self.result

def test_getUser(mocker: MockFixture):
    mockDB = mockDBconn()
    mock1 = mocker.patch("sqlite3.connect", return_value=mockDB)
    machine = fsm.FSM()
    testcases = [
        {"state": None, "parameters": {"uid":"user1",} , "expected": ('init', '')},
        {"state": ("user1", "記帳", "記帳"), "parameters": {"uid":"user1",} , "expected": ("user1", "記帳", "記帳")},
    ]

    for tc in testcases:
        # Arange
        mockDB.result = tc["state"]
        # Act
        res = machine.getUser(tc["parameters"]["uid"])
        # Assert
        assert res == tc["expected"]

def test_transit(mocker: MockFixture):
    mockDB = mockDBconn()
    mock1 = mocker.patch("sqlite3.connect", return_value=mockDB)
    machine = fsm.FSM()
    testcases = [
        {"parameters": {"state": '查詢月結餘', "input": '記帳', "data": '查詢月結餘',} , "expected": ('記帳', '記帳')},
        {"parameters": {"state": '查詢月結餘', "input": '$100', "data": '查詢月結餘',} , "expected": ('init', '')},
        {"parameters": {"state": '查看月結餘', "input": '$100', "data": '查看月結餘',} , "expected": ('查看月結餘', '查看月結餘')},
        {"parameters": {"state": '記帳:支出', "input": '記帳', "data": '記帳,支出',} , "expected": ('記帳', '記帳')},
        {"parameters": {"state": 'init', "input": '$100', "data": '',} , "expected": ('init', '')},
        {"parameters": {"state": '記帳', "input": '支出', "data": '記帳',} , "expected": ('記帳:支出', '記帳,支出')},
        {"parameters": {"state": '記帳', "input": '$100', "data": '記帳',} , "expected": ('記帳', '記帳')},
        {"parameters": {"state": '記帳', "input": '收入', "data": '記帳',} , "expected": ('記帳:收入', '記帳,收入')},
        {"parameters": {"state": '記帳:支出', "input": '食', "data": '記帳,支出',} , "expected": ('記帳:支出:類別', '記帳,支出,食')},
        {"parameters": {"state": '記帳:支出', "input": '*', "data": '記帳,支出',} , "expected": ('記帳:支出', '記帳,支出')},
        {"parameters": {"state": '記帳:支出:類別', "input": '$500', "data": '記帳,支出,食',} , "expected": ('記帳:支出:類別:金額', '記帳,支出,食,$500')},
        {"parameters": {"state": '記帳:支出:類別', "input": '500', "data": '記帳,支出,食',} , "expected": ('記帳:支出:類別', '記帳,支出,食')},
        {"parameters": {"state": '記帳:支出:類別:金額', "input": '便當', "data": '記帳,支出,食,$500',} , "expected": ('記帳:支出:類別:金額:備註', '記帳,支出,食,$500,便當')},
        {"parameters": {"state": '記帳:收入', "input": '$300', "data": '記帳,收入',} , "expected": ('記帳:收入:金額', '記帳,收入,$300')},
        {"parameters": {"state": '查詢當日收支', "input": '2024/04/01', "data": '查詢當日收支',} , "expected": ('查詢當日收支:日期', '查詢當日收支,2024/04/01')},
        {"parameters": {"state": '查詢當日收支', "input": '2024/02/31', "data": '查詢當日收支',} , "expected": ('查詢當日收支', '查詢當日收支')},
    ]

    for tc in testcases:
        # Arange
        # Act
        res = machine.transit(tc["parameters"]["state"],
                                tc["parameters"]["input"],
                                tc["parameters"]["data"])
        # Assert
        assert res == tc["expected"]


def test_verify(mocker: MockFixture):
    mockDB = mockDBconn()
    mock1 = mocker.patch("sqlite3.connect", return_value=mockDB)
    machine = fsm.FSM()
    testcases = [
        {"state": ('記帳:支出:類別:金額', '記帳,支出,食,$500'), "parameters": {"uid":"user1", "input": "我是備註"} , "expected": (True, '記帳:支出:類別:金額:備註', '記帳,支出,食,$500,我是備註')},
        {"state": ('init', ''), "parameters": {"uid":"user1", "input": "查詢當日收支"} , "expected": (False, '查詢當日收支', '查詢當日收支')},
    ]

    for tc in testcases:
        # Arange
        mockDB.result = tc["state"]
        # Act
        res = machine.verify(tc["parameters"]["uid"], tc["parameters"]["input"])
        # Assert
        assert res == tc["expected"]