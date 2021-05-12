from config import *
from flask import *

reminder = Blueprint('reminder', __name__)


@reminder.route('/remindergeturl', methods=['POST', 'GET'])
def remindergeturl():
    return render_template('Reminder/remindergeturl.html')


@reminder.route('/reminderindex', methods=['POST', 'GET'])
def reminderindex():
    id = request.form['userId']

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("SELECT * FROM reminders WHERE id_user == '{}'".format(id))
    all_product = c.fetchall()

    if all_product == []:
        return render_template('Reminder/reminder.html', reminder='', date=None)
    else:
        for i in all_product:
            service_1 = i[2]
            service_2 = i[3]
            service_3 = i[4]
            service_4 = i[5]
            reminder = i[6]
            date = i[7]
            time = i[8]
            print(service_1)
        return render_template('Reminder/reminder.html', service_1=service_1, service_2=service_2, service_3=service_3,
                               service_4=service_4,
                               reminder=reminder, date=date, time=time)


@reminder.route('/checkreminder', methods=['POST'])
def checkreminder():
    id = None
    userId = request.form['userId']
    reminder = request.form['reminder']
    date = request.form['date']
    time = request.form['time']

    service_1 = request.form.getlist('service_1')
    if len(service_1) > 0:
        service_1 = 1
    else:
        service_1 = 0
    service_2 = request.form.getlist('service_2')
    if len(service_2) > 0:
        service_2 = 1
    else:
        service_2 = 0
    service_3 = request.form.getlist('service_3')
    if len(service_3) > 0:
        service_3 = 1
    else:
        service_3 = 0
    service_4 = request.form.getlist('service_4')
    if len(service_4) > 0:
        service_4 = 1
    else:
        service_4 = 0

    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute("""INSERT INTO reminders VALUES(?,?,?,?,?,?,?,?,?)""",
                  (id, userId, service_1, service_2, service_3, service_4, reminder, date, time))
        conn.commit()
    except:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute(
            """Update reminders set service_1 = ?,service_2 = ?, service_3 = ?, service_4 = ?,reminder_user = ?, date_user = ?, time_user = ? WHERE id_user = ?""",
            (service_1, service_2, service_3, service_4, reminder, date, time, userId))
        conn.commit()

    return render_template('close.html')
