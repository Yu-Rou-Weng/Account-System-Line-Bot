import sqlite3
import re
import datetime

def consume(input):
    return input == "支出"
def income(input):
    return input == "收入"
def amount(input):
    pattern = re.compile(r"\$(\d+)")
    match = pattern.match(input)
    if match:
        return True
    else:
        return False
def classify(input):
    return input in ["食", "衣", "住", "行", "育", "樂"]
def direct_pass(input):
    return True
def is_date(input):
    pattern = re.compile(r"(\d+)/(\d+)/(\d+)")
    match = pattern.match(input)
    if match:
        tmp = match.groups()
        try:
            datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
            return True
        except Exception as e:
            return False
    else:
        return False

class FSM():
    def __init__(self):
        self.mapping = {
            "記帳": {
                consume: "記帳:支出",
                income: "記帳:收入",
            },
            "記帳:收入": {
                amount: "記帳:收入:金額"
            },
            "記帳:收入:金額": {
            },
            "記帳:支出": {
                classify: "記帳:支出:類別"
            },
            "記帳:支出:類別": {
                amount: "記帳:支出:類別:金額"
            },
            "記帳:支出:類別:金額": {
                direct_pass: "記帳:支出:類別:金額:備註"
            },
            "記帳:支出:類別:金額:備註": {
            },
            "查詢當日收支": {
                is_date: "查詢當日收支:日期"
            },
            "查詢當日收支:日期": {
            },
            "查詢月結餘": {
            }
        }
        self.accept_states = ["記帳:收入:金額", "記帳:支出:類別:金額:備註", "查詢當日收支:日期", "查詢月結餘"]
        self.funct_keywords = ["記帳", "查詢當日收支", "查詢月結餘"]
        self.delim = ','
        self.con = sqlite3.connect("state.db", check_same_thread=False)
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS fsm(id PRIMARY KEY, state, data)")
        self.con.commit()
    def getUser(self, uid):
        cur = self.con.cursor()
        res = cur.execute(f"SELECT state, data FROM fsm WHERE id='{uid}'")
        entry = res.fetchone()
        if entry:
            return entry
        else:
            return ('init', '')
    def transit(self, state, input, data):
        if state in self.accept_states:
            state = 'init'
            data = ''
        next_state = state
        new_data = data
        print(state)
        if input in self.funct_keywords:
            next_state = input
            new_data = input
        elif state == 'init':
            pass
        elif state in self.mapping.keys():
            for key in self.mapping[state].keys():
                if key(input):
                    next_state = self.mapping[state][key]
                    if data:
                        new_data = data + self.delim + input
                    else:
                        new_data = input
                    break
        else:
            pass
        return (next_state, new_data)
    def verify(self, uid, input):
        # get the current state of User from db
        state, data = self.getUser(uid)
        # transit to next state
        next_state, new_data = self.transit(state, input, data)
        # store back to database
        cur = self.con.cursor()
        cur.execute(f"REPLACE INTO fsm(id, state, data) VALUES ('{uid}','{next_state}','{new_data}')")
        self.con.commit()
        # Reply LineBot if the state is in the set of accept states
        return (next_state in self.accept_states, next_state, new_data)
    
a = FSM()
a.transit('查看月結餘', '$100', '查看月結餘')