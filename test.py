import sqlite3

# with sqlite3.connect("user.db") as con:
#      sql = ''' INSERT INTO reminders(id_user,reminder_user,datetime) VALUES(?,?,?) '''
#      cur = con.cursor()
#      cur.execute(sql, ('dasdad','asdasdsad','2020-15-20'))
#      con.commit()


conn = sqlite3.connect('user.db')
c = conn.cursor()
c.execute("""CREATE TABLE reminders(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             id_user TEXT UNIQUE,
             service_1 integer NOT NULL,
             service_2 integer NOT NULL,
             service_3 integer NOT NULL,
             service_4 integer NOT NULL,
             reminder_user TEXT,
             date_user DATETIME,
             time_user TIME
             )""")

# # conn = sqlite3.connect('user.db')
# # c = conn.cursor()
# # c.execute("""INSERT INTO reminders VALUES(?,?,?)""",
# #             ('dsadsad','adsadsad','2020-05-02'))
# # conn.commit()
#
#
# conn = sqlite3.connect('user.db')
# c = conn.cursor()
#
# c.execute("SELECT * FROM reminders")
# all_product = c.fetchall()
# for i in all_product:
#     print(i[0])
#     print(i[1])
#     print(i[2])
# print(all_product)
