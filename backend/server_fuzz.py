import atheris
import sys
import json
import flask

with atheris.instrument_imports():
    import server

# 初始化 Flask 應用
app = server.app.test_client()

def clean_string(s):
    return ''.join(c for c in s if not 0xD800 <= ord(c) <= 0xDFFF)

def test_one_input(data):
    fdp = atheris.FuzzedDataProvider(data)

    # 隨機選擇測試的 API 端點
    endpoints = ['/api/transaction', '/api/balance/month', '/get_users']
    endpoint = fdp.PickValueInList(endpoints)

    if endpoint == '/api/transaction':
        method_type = fdp.PickValueInList(['GET', 'POST'])
        if method_type == 'GET':
            # 生成 GET 請求的參數
            year = str(fdp.ConsumeIntInRange(2020, 2024))
            month = str(fdp.ConsumeIntInRange(1, 12))
            day = str(fdp.ConsumeIntInRange(1, 31))
            username = clean_string(fdp.ConsumeString(10)) or "defaultUser"
            response = app.get(f'{endpoint}?year={year}&month={month}&day={day}&id={username}')
        else:
            # 生成 POST 請求的參數
            username = clean_string(fdp.ConsumeString(10)) or "defaultUser"
            iotype = fdp.PickValueInList(['收入', '支出'])
            consume_type = fdp.PickValueInList(['食', '衣', '住', '行', '育', '樂', '無'])
            amount = str(fdp.ConsumeIntInRange(1, 10000))
            time_year = str(fdp.ConsumeIntInRange(2020, 2024))
            time_month = str(fdp.ConsumeIntInRange(1, 12))
            time_date = str(fdp.ConsumeIntInRange(1, 31))
            remark = clean_string(fdp.ConsumeString(50))
            response = app.post(endpoint, data={
                'id': username, 'iotype': iotype, 'consume_type': consume_type, 
                'amount': amount, 'time_year': time_year, 'time_month': time_month, 
                'time_date': time_date, 'remark': remark
            })

    elif endpoint == '/api/balance/month':
        year = str(fdp.ConsumeIntInRange(2020, 2024))
        month = str(fdp.ConsumeIntInRange(1, 12))
        username = clean_string(fdp.ConsumeString(10)) or "defaultUser"
        response = app.get(f'{endpoint}?id={username}&time_year={year}&time_month={month}')

    elif endpoint == '/get_users':
        response = app.get(endpoint)

    print(f"Status code: {response.status_code} for endpoint: {endpoint}")

def main():
    atheris.Setup(sys.argv, test_one_input)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
