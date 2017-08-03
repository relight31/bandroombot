#import modules used here
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler
from db_helper import *

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

#states
big_brother = True
active_sessions = {}
admin_id = {85548066} #Russell
unauth_user_msg = "Sorry {}, you do not have access to this function."

def bigbrothertoggle(bot,update):#not working
    global big_brother
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    if user_id in admin_id:
        if big_brother:
            big_brother = False
            bot.send_message(chat_id=update.message.chat_id,\
            text="Big Brother mode: OFF")
        else:
            big_brother = True
            bot.send_message(chat_id=update.message.chat_id,\
            text="Big Brother mode: ON")
    else:
        bot.send_message(chat_id=update.message.chat_id, \
        text=unauth_user_msg.format(user_name))

def workinprogress(bot, update):
    user_name = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text="Sorry {}, this\
    function is not ready yet.".format(user_name))

def whoami(bot, update):
    user_name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    chat_idno = update.message.chat_id
    bot.send_message(chat_id=update.message.chat_id, \
    text="user = {}, id = {}, chat_id = {}".format(user_name, user_id, chat_idno))

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

def idk(bot, update):
    response = update.message.text
    bot.send_message(chat_id=update.message.chat_id,\
    text="I'm sorry, I don't understand what you mean by '{}'.".format(response))

# Functions and states for newbooking
CCA, TIME, REASON, CONFIRM = range(4)

def newbooking_start(bot,update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if user_id in active_sessions:
        pass
    else:
        #create session
        session = {'name':user_name, 'return_id':user_id}
        active_sessions[user_id] = session
        #fill session
        cca_keyboard = [
            [InlineKeyboardButton('Aca', callback_data='cca.Aca'),\
            InlineKeyboardButton('Amplitude', callback_data='cca.Amplitude')],
            [InlineKeyboardButton('Band', callback_data='cca.Band'),\
            InlineKeyboardButton('Choir', callback_data='cca.Choir')],
            [InlineKeyboardButton('Ensemble', callback_data='cca.Ensemble'),\
            InlineKeyboardButton('Xinyao', callback_data='cca.Xinyao')]
        ]
        reply_markup = InlineKeyboardMarkup(cca_keyboard)
        message_text = "Hi {}, let's start a new booking.\
        BTW you can cancel this current booking at any time using /cancel.\
        \n\nPlease select your cca."
        user_name = update.message.from_user.first_name
        bot.send_message(chat_id=update.message.chat_id, \
        text=message_text.format(user_name), reply_markup=reply_markup)
        return CCA

def newbooking_gettime(bot, update):
    query = update.callback_query
    chosen_cca = query.data[4:]
    user_id = query.message.chat_id
    active_sessions[user_id]['cca']=chosen_cca
    bot.edit_message_reply_markup(chat_id=query.message.chat_id,\
    message_id=query.message.message_id)
    message_content = "You are booking under {}.\n\n\
    Please enter the date and time you would like to book the Band Room for.\
    Keep your bookings max 3 hours long so that others have a chance to use \
    the room for their practices too.\n\n\
    You can place multiple bookings in one go. eg. 24 Sep 7pm - 9pm, 24 Sep 1900 - 2100 etc "
    bot.send_message(chat_id=query.message.chat_id,\
    text=message_content.format(chosen_cca))
    return TIME

def newbooking_getreason(bot, update):
    user_id = update.message.from_user.id
    chosen_time = update.message.text
    active_sessions[user_id]['time']=chosen_time
    user_name = update.message.from_user.first_name
    message_content = "You are booking from {0}.\n\n\
    Ok {1}, now please tell me your purpose of this booking.\n\n\
    eg. rehearsal for NOTA, sectional practice etc."
    bot.send_message(chat_id=update.message.chat_id, \
    text=message_content.format(chosen_time, user_name))
    return REASON

def newbooking_confirm(bot, update):
    chosen_reason = update.message.text
    user_id = update.message.from_user.id
    active_sessions[user_id]['reason']=chosen_reason
    user_name = active_sessions[user_id]['name']
    cca = active_sessions[user_id]['cca']
    time = active_sessions[user_id]['time']
    reason = active_sessions[user_id]['reason']
    message_content = "Ok {0}, just to confirm, you are placing a booking for \
    {1}, from {2} for the purpose of {3}.\n\n\
    Is that correct?"
    keyboard = [
        [InlineKeyboardButton('Yes', callback_data='{}.yes'.format(user_id)),\
        InlineKeyboardButton('No', callback_data='{}.no'.format(user_id))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id,\
    text=message_content.format(user_name,cca,time,reason),\
    reply_markup=reply_markup)

def parse_id(string):
    counter = 0
    found = False
    while not found:
        test = string[counter]
        if test == '.':
            found = True
        else:
            counter += 1
    return counter

def newbooking_finalise(bot, update):
    query = update.callback_query
    bot.edit_message_reply_markup(chat_id=query.message.chat_id,\
    message_id=query.message.message_id)
    dot = parse_id(query.data)
    user_id = int(query.data[:dot])
    response = query.data[(dot+1):]
    user_name = active_sessions[user_id]['name']
    if response == 'yes':
        bot.send_message(chat_id=query.message.chat_id,\
        text="Ok, give me a moment to place your booking.")
        #try add to db
        try:
            booking = active_sessions[user_id]
            make_booking(booking)
        except:
            bot.send_message(chat_id=query.message.chat_id,\
            text="Sorry {}, I have run into a problem placing your booking.\
            \n\nCan you try placing a booking again using /newbooking?".format(user_name))
        else:
            bot.send_message(chat_id=query.message.chat_id,\
            text="I have successfully placed your booking, {}.\
            I will contact you again soon to let you know if your booking has been\
            approved or rejected. Thank you for using KE Band Room Bot!".format(user_name))
        finally:
            del active_sessions[user_id]
            return ConversationHandler.END
    elif response == 'no':
        del active_sessions[user_id]
        bot.send_message(chat_id=query.message.chat_id,\
        text="Alright {}, I have cancelled your booking. If you wish to make a \
        new booking, you can simply type /newbooking again. \
        See you soon!".format(user_name))
        return ConversationHandler.END
    else:
        bot.send_message(chat_id=query.message.chat_id,\
        text="I'm sorry, I don't understand what you mean. \
        Could we start again with /newbooking?")
        return ConversationHandler.END

def newbooking_cancel(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    del active_sessions[user_id]
    bot.send_message(chat_id=update.message.chat_id,\
    text="Alright {}, I have cancelled your booking. If you wish to make a \
    new booking, you can simply type /newbooking again. \
    See you soon!".format(user_name))
    return ConversationHandler.END

#functions for approval

def view_init(bot, update):
    requesting_user = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if requesting_user in admin_id:
        try:
            bookings = pull_newbookings()
        except:
            bot.send_message(chat_id=requesting_user,\
            text='I have encountered an error {}, please try again.'.format(user_name))
        else:
            if len(bookings) <= 0:
                bot.send_message(chat_id=requesting_user,\
                text='You have no pending bookings, {}.'.format(user_name))
            else:
                keyboard = [
                    [InlineKeyboardButton('Yes', callback_data='yesiwanttosee'),\
                    InlineKeyboardButton('No', callback_data='nodontwant')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                number_of_bookings = len(bookings)
                bot.send_message(chat_id=requesting_user,\
                text="You have {} pending bookings, want to review now?".format(str(number_of_bookings)),\
                reply_markup=reply_markup)
    else:
        bot.send_message(chat_id=update.message.chat_id,\
        text=unauth_user_msg.format(user_name))

def view_seebookings(bot, update):
    query = update.callback_query
    bot.edit_message_reply_markup(chat_id=query.message.chat_id,\
    message_id=query.message.message_id)
    if query.data == 'yesiwanttosee':
        bookings = pull_newbookings()
        for booking in bookings:
            displaybooking(booking)
    elif query.data == 'nodontwant':
        bot.send_message(chat_id=update.message.chat_id,\
        text='Ok then, see you again soon.')
    else:
        bot.send_message(chat_id=update.message.chat_id,\
        text='What are you doing.')

def displaybooking(booking): #temporary fix
    booking_id = booking[0]
    name = booking[1]
    cca = booking[3]
    time = booking[4]
    reason = booking[5]
    return_id = booking[2]

    keyboard = [
        [InlineKeyboardButton('Approve', callback_data='apprej.1.{}'.format(booking_id)),\
        InlineKeyboardButton('Reject', callback_data='apprej.2.{}'.format(booking_id))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text='''
    Booking no:{0}
    Return ID: {5}
    {1} from {2} booking {3} for {4}.
    '''
    russ = 85548066
    bot.send_message(chat_id=russ, \
    text=text.format(booking_id, name, cca, time, reason, return_id),\
    reply_markup=reply_markup)

def view_bookingresponse(bot, update):
    query = update.callback_query
    if 'apprej.' in query.data:
        response = int(query.data[7]) # need to parse
        booking_id = int(query.data[9:])

        current = pull_specific(booking_id)

        name = current[1]
        cca = current[3]
        time = current[4]
        reason = current[5]
        return_id = current[2]

        if response == 1: #approved
            try:
                approve_booking(booking_id)
            except:
                #encoutered error
                pass
            else:
                #edit message
                message_to_booker = '''
                Booking S/N {0}: APPROVED

                Hi {1}, your booking on {2} for {3} under {4} has been approved.

                Please be reminded to adhere to the timings of your booking \
                and return the band room to a neat and tidy state before leaving.

                Thank you and enjoy the band room :)
                '''
                bot.send_message(chat_id=return_id,\
                text=message_to_booker.format(booking_id, name, time, reason, cca))
            pass
        elif response == 2: #rejected
            try:
                reject_booking(booking_id)
            except:
                # encounter error
                pass
            else:
                # edit message
                # send message
                pass
            pass
        else:
            pass
    else:
        pass

# functions for amend
def amend_pullbookings(bot, update):
    pass

def amend_options(bot,update):
    pass

def amend_action(bot, update):
    pass
