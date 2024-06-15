from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.models import CarouselTemplate,  CarouselColumn
from urllib.parse import parse_qsl
import requests
from fsm import FSM
import datetime


 
#======python的函數庫==========

app = Flask(__name__)  
fsm = FSM()
 
LINE_CHANNEL_ACCESS_TOKEN = '89XGUDK8/Clvg+tLuPa858oIrRxUQGY6tJ3+mrRBx4AmE2wZXv738wdevR1He3M9wRNIrWL/ntNjbdHe/ZeEbyP9oKFwD3vVBcrpE/BGrnk1pdscxXzfnA2Kpt/wIjCdo4E6CaC2SPov6YodrFiJNQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '8051d1eee39f087756b6ad0ebf2c4d0e'
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

def sendDatetime(event):
    try:
        message =  TemplateSendMessage(
            alt_text = "單日查詢",
            template = ButtonsTemplate(
            thumbnail_image_url='https://i.imgur.com/yMS2lJI.jpg',
                title='單日查詢',
                text='請選擇：',
                actions=[
                    DatetimePickerTemplateAction(
                        label = "選取日期",
                        data = "action=sell_date&mode=date",
                        mode = "date",
                        initial = "2024-09-24",
                        min = "2024-01-01",
                        max = "2024-12-31"
                    )
                ]
                    
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendData_sell(event, backdata):
    try:
        if backdata.get('mode') == 'date':
            dt = '日期為：'+ event.postback.params.get('date')
        elif backdata.get('mode') == 'time':
            dt = '時間為：'+ event.postback.params.get('time')

        elif backdata.get('mode') == 'datetime':
            dt = datetime.datetime.strptime(event.postback.params.get('datetime'), '%Y-%m-%dT%H:%M')
            
            dt = dt.strftime('{d}%Y-%m-%d, {t}%H:%M').format(d='日期為:', t='時間為:')

        message = TextSendMessage(
            text = dt
        )
        
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤!'))

def sendMonthPicker(event):
    try:
        message = TemplateSendMessage(
            alt_text="選擇月份",
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/yMS2lJI.jpg',
                        title='選擇月份',
                        text='請選擇月份：',
                        actions=[
                            PostbackTemplateAction(label='1月', data='action=query_balance&month=1'),
                            PostbackTemplateAction(label='2月', data='action=query_balance&month=2'),
                            PostbackTemplateAction(label='3月', data='action=query_balance&month=3')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/yMS2lJI.jpg',
                        title='選擇月份',
                        text='請選擇月份：',
                        actions=[
                            PostbackTemplateAction(label='4月', data='action=query_balance&month=4'),
                            PostbackTemplateAction(label='5月', data='action=query_balance&month=5'),
                            PostbackTemplateAction(label='6月', data='action=query_balance&month=6')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/yMS2lJI.jpg',
                        title='選擇月份',
                        text='請選擇月份：',
                        actions=[
                            PostbackTemplateAction(label='7月', data='action=query_balance&month=7'),
                            PostbackTemplateAction(label='8月', data='action=query_balance&month=8'),
                            PostbackTemplateAction(label='9月', data='action=query_balance&month=9')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/yMS2lJI.jpg',
                        title='選擇月份',
                        text='請選擇月份：',
                        actions=[
                            PostbackTemplateAction(label='10月', data='action=query_balance&month=10'),
                            PostbackTemplateAction(label='11月', data='action=query_balance&month=11'),
                            PostbackTemplateAction(label='12月', data='action=query_balance&month=12')
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except Exception as e:
        print(f'Error: {str(e)}')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='發生錯誤！'))

def accoutingButton(event):
    message = TemplateSendMessage(
            alt_text = "記帳按鈕",
            template=ButtonsTemplate(
                title = "記帳種類",
                text = "請選擇：",
                actions = [
                    MessageTemplateAction(
                            label='食',
                            text='食'
                        ),
                    MessageTemplateAction(
                            label='衣',
                            text='衣'
                        ),
                    MessageTemplateAction(
                            label='住',
                            text='住'
                        ),
                    MessageTemplateAction(
                            label='行',
                            text='行'
                        ),

                ]
            )
        )
    line_bot_api.reply_message(event.reply_token, message)

def chooseAccountTypeButton(event):
    message = TemplateSendMessage(
            alt_text = "記帳按鈕",
            template=ButtonsTemplate(
                title = "收入\支出",
                text = "請選擇：",
                actions = [
                    MessageTemplateAction(
                            label='收入',
                            text='收入'
                        ),
                    MessageTemplateAction(
                            label='支出',
                            text='支出'
                        ),

                ]
            )
        )
    line_bot_api.reply_message(event.reply_token, message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    mtext = event.message.text
    UserId = event.source.user_id
    state_info = fsm.verify(UserId, mtext)
    #print(state_info)
    
    if mtext == "記帳":
        chooseAccountTypeButton(event)
    elif mtext == "查詢當日收支":
        sendDatetime(event)
    elif mtext == "查詢月結餘":
        sendMonthPicker(event)
    elif mtext == "食" or mtext == "衣" or mtext == "住" or mtext == "行":
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入金額"))
    elif mtext == "收入" or mtext == "支出":
        if mtext == "支出":
            accoutingButton(event)
        elif mtext == "收入":
            line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入本日收入"))
    elif mtext[0] == '$' and mtext[1:].isdigit() and state_info[0] != True:
        line_bot_api.reply_message(event.reply_token, TextSendMessage("請輸入備註"))
    else:
        msg=str(event.message.text)
        profile = line_bot_api.get_profile(UserId)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(profile.display_name +  "說: "+ msg))

    if state_info[0] == True and state_info[1].count("記帳"):
        now = datetime.datetime.now()
        current_year = now.year
        current_month = now.month
        current_day = now.day

        if state_info[1].count("收入"):
            _, iotype, amount = state_info[2].split(',')
            consume_type = "無"
            remark = "無"
        else:
            _, iotype, consume_type, amount, remark = state_info[2].split(',')
        
        amount = amount[1:]
        url = f"http://localhost:5000/api/transaction?id={UserId}&iotype={iotype}&consume_type={consume_type}&amount={amount}&time_year={current_year}&time_month={current_month}&time_date={current_day}&remark={remark}"
        print("url = ", url)
        response = requests.post(url)
        if response.status_code == 200:
            line_bot_api.push_message(UserId, TextSendMessage(text='資料寫入成功!'))
            print("Response:", response.text)
        else:
            line_bot_api.push_message(UserId, TextSendMessage(text='資料寫入成功!'))

@handler.add(PostbackEvent)
def handle_message(event):
    backdata = dict(parse_qsl(event.postback.data))  # 取得Postback資料
    UserId = event.source.user_id
    if backdata.get('action') == 'sell_date':
        date = event.postback.params.get("date")
        year, month, day = date.split('-')
        url = f"http://localhost:5000/api/transaction?id={UserId}&year={year}&month={month}&day={day}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                transactions = response.json()['records']
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(transactions)))
            except ValueError:
                print("Response not in JSON format.")
                print("Response:", response.text)
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="本日無資料"))
            print("Failed to get data:", response.status_code)
            print("Response:", response.text)

    if backdata.get('action') == 'query_balance':
        month = backdata['month']
        url = f"http://localhost:5000/api/balance/month?id={UserId}&year=2024&month={month}"
        response = requests.get(url)
        if response.status_code == 200:
            try:
                transactions = response.json()
                month_balance = transactions.get('month balance')  # 取出月結餘的值
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"本月餘額為: {month_balance}"))
            except ValueError:
                print("Response not in JSON format.")
                print("Response:", response.text)
        elif response.status_code == 404:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="本月無資料"))
        else:
            print("Failed to get data:", response.status_code)
            print("Response:", response.text)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port,debug=True)