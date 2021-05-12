from line import *
from assessment import *
from reminder import *
from config import *
import datetime
import requests
###############################################################################
from apscheduler.schedulers.background import BackgroundScheduler


def test():
    x = datetime.datetime.now()
    y = x.strftime("%Y")
    m = x.strftime("%m")
    d = x.strftime("%d")
    sum = y + '-' + m + '-' + d
    h = x.strftime("%H")
    m = x.strftime("%M")
    timex = h + ':' + m
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reminders WHERE date_user == '{}'".format(sum))
    all_product = c.fetchall()
    print(all_product)
    for i in all_product:
        if i[8] == timex:
            id = i[1]
            service_1 = i[2]
            service_2 = i[3]
            service_3 = i[4]
            service_4 = i[5]
            reminder = i[6]
            date = i[7]
            time = i[8]
            if service_1 == 1:
                txt1 = '✅ ไปตามนัดพบแพทย์'
            else:
                txt1 = '❌ ไปตามนัดพบแพทย์'
            if service_2 == 1:
                txt2 = '✅ ไปตามนัดรับยาเดิม'
            else:
                txt2 = '❌ ไปตามนัดรับยาเดิม'
            if service_3 == 1:
                txt3 = '✅ ไปตามนัดเข้ากลุ่มบำบัด'
            else:
                txt3 = '❌ ไปตามนัดเข้ากลุ่มบำบัด'
            if service_4 == 1:
                txt4 = '✅ ขอคำปรึกษาปัญหาครอบครัว'
            else:
                txt4 = '❌ ขอคำปรึกษาปัญหาครอบครัว'
            text_message = TextSendMessage(
                text='⏰ แจ้งเตือน\n{}\n{}\n{}\n{}\nวันที่ : {}\nเวลา : {}\nหมายเหตุอื่นๆ : {}'.format(txt1, txt2, txt3,
                                                                                                      txt4, date, time,
                                                                                                      reminder))
            line_bot_api.push_message(id, text_message)


sched = BackgroundScheduler(daemon=True)
sched.add_job(func=test, trigger='cron', minute='*')
# sched.add_job(test,'cron',hour='21',minute='51')
sched.start()
################################################################################

app = Flask(__name__)
app.register_blueprint(assessment)
app.register_blueprint(reminder)
app.secret_key = 'secertkey'


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)  # รับ data จาก Line api
    req = json.loads(body)  # แปลง data เป็น json
    print(req)
    type_text = req["events"][0]["message"]["type"]  # ตัวแปรดึงชนิดของข้อความที่ได้รับ
    reply_Token = req['events'][0]['replyToken']
    id = req['events'][0]['source']['userId']
    print(type_text)
    print(reply_Token)
    print(id)
    if type_text == 'sticker':
        # keywords = req["events"][0]["message"]['keywords']
        # print(keywords)
        req['events'][0]['message']['type'] = 'text'
        req['events'][0]['message']['text'] = 'sticker'
        requests.post(dialogflow, json=req)  # ส่งข้อมูลไปยัง dialogflow
    else:
        text = req['events'][0]['message']['text']  # ตัวแปรดึง text
        print(text)
        requests.post(dialogflow, json=req)  # ส่งข้อมูลไปยัง dialogflow
    return req


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]  ## intent จาก dialogflow
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']  ## คำที่ส่งมา
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']  ## reply_token
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']  ## id ผู้ส่ง
    disname = line_bot_api.get_profile(id).display_name  ## แสดงชื่อ
    print(req)
    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)

    if intent == 'Question':  # สอบถามปัญหา
        Question(text, intent, reply_token, id, req)
    if intent == 'Menu' or 'Menu - yes':  # เมนู
        Menu(text, intent, reply_token, id)
    if intent == 'Reminder':  # เตือนความจำ
        Reminder(text, intent, reply_token, id)
    if intent == 'Drug':  # รู้เรื่องยา
        Drug(text, intent, reply_token, id)
    if intent == 'Knowledge':  # เกร็ดความรู้
        Knowledge(text, intent, reply_token, id)
    if intent == 'AssessmentForm':  # แบบประเมิน
        AssessmentForm(text, intent, reply_token, id)
    if intent == 'Public relations':  # ติดต่อ ประชาสัมพันธ์
        Public_relations(text, intent, reply_token, id)
    else:
        reply(text, intent, reply_token, id, req)
    return req


if __name__ == '__main__':
    app.run(debug=True, port=3180, use_reloader=False)
