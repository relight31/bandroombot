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

def end_session(bot, update):
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
