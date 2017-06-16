start_text = "Hi {}! I am the KE Band Room Bot.\
\n\nI can assist you with booking the Band Room for rehearsals or trainings.\
\n\nTo place a booking, type /newbooking."

help_text = "Here is a list of commands you can give me.\
\n\n/newbooking: Place a booking for the Band Room.\
\n/checkstatus: Check if your bookings have been approved.\
\n/amend: Amend details of your pending bookings. \
(You may not amend bookings after they have been approved/rejected)\
\n/cancel: Cancel any pending bookings you have placed.\
\n\n/help: View this guide again."

active_sessions = {}
admin_id = 85548066
unauth_user_msg = "Sorry {}, you do not have access to this function."
def workinprogress(bot, update):
    user_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text="Sorry {}, this \
    function is not ready yet.".format(user_name))

def whoami(bot, update):
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    bot.send_message(chat_id=update.message.chat_id, \
    text="user = {}, id = {}".format(user_name, user_id))

def unknown(bot, update):
    user_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, \
    text="Sorry {}, I do not understand that command.".format(user_name))

def start(bot, update):
    user_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, \
    text=start_text.format(user_name))

def tutorial(bot, update):
    bot.send_message(chat_id=update.message.chat_id, \
    text=help_text)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def open_session(bot, update):
    id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if id in active_sessions:
        bot.send_message(chat_id=update.message.chat_id, \
        text="You already have an open session, {}.".format(user_name))
        if dev_mode:
            print("Session already open")
    else:
        session = {}
        active_sessions[id] = session
        bot.send_message(chat_id=update.message.chat_id, \
        text="Session for {} created.".format(user_name))
        if dev_mode:
            print("Session created")

def end_session(bot, update): #need to find new session tracking
    id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if id in active_sessions:
        del active_sessions[id]
        bot.send_message(chat_id=update.message.chat_id, \
        text="Your session was ended successfully.")
        if dev_mode:
            print("Session ended")
    else:
        bot.send_message(chat_id=update.message.chat_id, \
        text="You do not currently have an active session, {}.".format(user_name))
        if dev_mode:
            print("No active sessions")
