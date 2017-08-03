import sqlite3

test = {'name':'Russell',
        'return_id': 123123123,
        'cca':"CMB",
        'time':'24 sep',
        'reason':'testing'
        }

def make_booking(booking):
    #assuming clean inputs
    name = booking['name']
    user_id = booking['return_id']
    cca = booking['cca']
    time = booking['time']
    reason = booking['reason']
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bookings \
(name, user_id, cca, time, reason, approved) VALUES(?,?,?,?,?,?)',\
                         (name, user_id, cca, time, reason, 0))
    conn.commit()
    conn.close()

def pull_newbookings():
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE approved=?', (0,))
    results = cursor.fetchall()
    conn.close()
    return results

def pull_specific(booking_id):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,))
    results = cursor.fetchone()
    conn.close()
    return results

def booking_search(**kwargs):
    pass

def approve_booking(booking_id):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET approved = 1 WHERE booking_id = ?', (booking_id,))
    conn.commit()
    conn.close()

def reject_booking(booking_id):
    conn = sqlite3.connect('bot_db.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET approved = 2 WHERE booking_id = ?', (booking_id,))
    conn.commit()
    conn.close()

def amend_booking(booking_id):
    pass
