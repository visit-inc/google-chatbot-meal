import os
from flask import Flask
import threading
import schedule
import requests
import time

from json import dumps
from httplib2 import Http

app = Flask(__name__)

@app.route('/health')
def health_check():
    return "OK"

def run_flask_app():
    app.run(host='0.0.0.0', port=8080, use_reloader=False)

def send_message(text):
    url = os.environ.get("WEBHOOK_URL")
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    message_json = {"text": text}  # 메시지를 JSON 형식으로 변환
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(message_json),  # JSON 데이터를 문자열로 변환
    )

def run_scheduled_jobs():
    schedule.run_pending()

def send_lunch_order_reminder():
    send_message("배달 음식 시키실 분은 메뉴를 취합해주세요!")

def send_lunch_reminder():
    send_message("점심 시간이에요, 다들 업무 잠시 중단하고 영양분 채우고 옵시다!")

def send_lunch_end_reminder():
    send_message("점심시간이 종료되었습니다. 다들 슬슬 자리로 돌아가서 다시 업무 시작 해볼까요?")

def send_friday_lunch_end_reminder():
    send_message("금요일은 점심시간이 1시간이에요. 이른 퇴근인만큼 다시 자리로 돌아가 빡시게 일해볼까요?")
    
# 스케줄 설정
noti_11 = "02:00"
noti_12 = "03:00"
noti_13 = "04:00"
noti_1330 = "04:30"

schedule.every().monday.at(noti_11).do(send_lunch_order_reminder)
schedule.every().tuesday.at(noti_11).do(send_lunch_order_reminder)
schedule.every().wednesday.at(noti_11).do(send_lunch_order_reminder)
schedule.every().thursday.at(noti_11).do(send_lunch_order_reminder)
schedule.every().friday.at(noti_11).do(send_lunch_order_reminder)

schedule.every().monday.at(noti_12).do(send_lunch_reminder)
schedule.every().tuesday.at(noti_12).do(send_lunch_reminder)
schedule.every().wednesday.at(noti_12).do(send_lunch_reminder)
schedule.every().thursday.at(noti_12).do(send_lunch_reminder)
schedule.every().friday.at(noti_12).do(send_lunch_reminder)

schedule.every().monday.at(noti_1330).do(send_lunch_end_reminder)
schedule.every().tuesday.at(noti_1330).do(send_lunch_end_reminder)
schedule.every().wednesday.at(noti_1330).do(send_lunch_end_reminder)
schedule.every().thursday.at(noti_1330).do(send_lunch_end_reminder)

schedule.every().friday.at(noti_13).do(send_friday_lunch_end_reminder)

# schedule.every(1).minute.do(test)

def send_mail():
    # 무한 루프로 스케줄 유지
    while True:
        run_scheduled_jobs()

if __name__ == '__main__':
    # Flask 앱을 별도의 스레드에서 실행
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    # 메일 발송 기능 실행
    send_mail()
