import sqlite3

conn = sqlite3.connect('bot_db.db')
cursor = conn.cursor()

# booking_id, name, user_id, cca, reason, start, finish, approved

cursor.execute('UPDATE bookings SET approved = (?) WHERE booking_id = 1', (None,))
conn.commit()

cursor.execute("SELECT * FROM bookings")
print(cursor.fetchone())

def make_booking(name, user_id, cca, reason, start, finish, approved):
    #assuming clean inputs
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor('INSERT INTO bookings VALUES(?,?,?,?,?,?,?)',\
                         (name, user_id, cca, reason, start, finish, approved))
    cursor.execute()
    conn.commit()
    conn.close()
