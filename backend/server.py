from flask import Flask, jsonify, request
import repo.db
from repo.db import postgresDB
import psycopg2
import time
from psycopg2 import sql

app = Flask(__name__)

while True:
    try:
        db = repo.db.postgresDB()
        db.connect()
        break
    except psycopg2.Error as e:
        app.logger.info(f'An error occurred: {e}')
    time.sleep(10)

#time.sleep(10)

try:
    with open('./model/schema.sql', 'r', encoding='utf-8') as file:
        schema_sql = file.read()
        print(schema_sql)
        db.execute_stmt(schema_sql, (), False)
except Exception as e:
        print(f"An error occurred: {e}")
try:
    with open('./model/init.sql', 'r', encoding='utf-8') as file:
        sql = file.read()
        print(sql)
        db.execute_stmt(sql, (), False)
except Exception as e:
        print(f"An error occurred: {e}")


# @app.before_first_request
# def init():
#     try:
#         with open('./model/init.sql', 'r') as file:
#             sql = file.read()
#             print(sql)
#             db.execute_stmt(sql, (), False)
#     except Exception as e:
#             print(f"An error occurred: {e}")


@app.route('/')
def home():
    return "Hello world!"

@app.route('/health')
def ping():
    return jsonify({'msg': 'OK'}), 200

@app.route('/test')
def test():
    # data = request.get_json()
    # if json = {'uid': 1123423, 'username': 'test'} => data['username'] == 'test'
    ret = db.execute_stmt('SELECT * FROM users WHERE username=%s', ('test',), True)
    if ret != []:
        return jsonify({'msg': 'find the user'}), 200
    else:
        return jsonify({'msg': 'no such user'}), 201
        # the only user inserted is named 'Test' so no user named 'test'

@app.route('/api/transaction', methods=['GET'])
def get_transaction():
    year = request.args.get('year')
    month = request.args.get('month')
    day = request.args.get('day')
    username = request.args.get('id')
    id = get_id(username)
    try:
        query = 'SELECT rid, iotype, consume_type, amount, remarks FROM records WHERE id=%s AND time_year=%s AND time_month=%s AND time_date=%s'
        records = db.execute_stmt(query, (id, year, month, day), True)
        if records:
            formatted_records = f"{year}年{month}月{day}日\n-------------\n" + "\n".join(
                f"編號: {record[0]}\n收支: {record[1]}\n類別: {record[2]}\n金額: ${record[3]}\n備註: {record[4]}\n----------" 
                for record in records)
            return jsonify({'records': formatted_records}), 200
        else:
            return jsonify({'error': 'No records found'}), 404
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Data fetch failed'}), 500

@app.route('/api/transaction', methods=['POST'])
def post_transaction():
    username = request.args.get('id')
    id = get_id(username)
    iotype = request.args.get('iotype')
    consume_type = request.args.get('consume_type')
    amount = request.args.get('amount')
    time_year = request.args.get('time_year')
    time_month = request.args.get('time_month')
    time_date = request.args.get('time_date')
    remark = request.args.get('remark')
    query = "INSERT INTO records (id, iotype, consume_type, amount, time_year, time_month, time_date, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"#.format(id, iotype, consume_type, amount, time_year, time_month, time_date)
    records = db.execute_stmt(query, (id, iotype, consume_type, amount, time_year, time_month, time_date, remark), False)
    print("Database returned:", records)

    return jsonify({'id':id}), 200

@app.route('/api/balance/month', methods=['GET'])
def balance_month():
    year = request.args.get('year')
    month = request.args.get('month')
    username = request.args.get('id')
    id = get_id(username)
    try:
        query = 'SELECT * FROM records WHERE id=%s AND time_year=%s AND time_month=%s'
        records = db.execute_stmt(query, (id, year, month), True)
        
        if records:
            # Compute the sum of income and outcome
            in_sum = 0
            out_sum = 0
            for i in range(len(records)):
                if records[i][2] == '收入':
                    in_sum += records[i][4]
                elif records[i][2] == '支出':
                    out_sum += records[i][4]
            return jsonify({'month balance': in_sum - out_sum}), 200
        else:
            return jsonify({'error': 'No records found'}), 404
    except Exception as e:
        print(f"Error fetching data: {e}")
        return jsonify({'error': 'Data fetch failed'}), 500

@app.route('/get_users')
def get_users():
    db = postgresDB()
    db.connect()
    query = "SELECT * FROM users;"
    result = db.execute_stmt(query, None, True)
    db.close()
    return jsonify(result)

def get_id(username):
    select_query = 'SELECT * FROM users WHERE username=%s'
    ret = db.execute_stmt(select_query, (username,), True)
    if ret == []:
        insert_query = 'INSERT INTO users (username) VALUES (%s);'
        db.execute_stmt(insert_query, (username,), False)
        ret = db.execute_stmt(select_query, (username,), True)
    
    return ret[0][0]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
