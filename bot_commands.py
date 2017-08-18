#import modules used here
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler

start_text = '''
Hi {}! I am the KE CMB Bot.
If you need CMB to provide AV support for your event, I can help you place a request.
To place a request, type /newrequest."
'''

help_text = '''
Here is a list of commands you can give me.
/newbooking: Place a booking for the Band Room.
/checkstatus: Check if your bookings have been approved.
/help: View this guide again.
'''

#states
big_brother = True
active_sessions = {}
admin_id = {85548066:'Russell'}
cmb_head = 85548066
unauth_user_msg = "Sorry {}, you do not have access to this function."

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
PHONE, CCA, EVENT, VENUE, DATETIME, DESCRIPTION, CONFIRM = range(7)

def newrequest_start(bot,update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    if user_id in active_sessions:
        # don't cb
        pass
    else:
        #create session
        session = {'name':user_name, 'return_id':user_id}
        active_sessions[user_id] = session

        message_text = '''
        Hi {}, let's start a new request.

        Can I have your phone number?

        BTW you can cancel this current booking at any time with /cancel.
        '''
        bot.send_message(chat_id=update.message.chat_id, \
        text=message_text.format(user_name))
        return PHONE

def newrequest_getcca(bot, update):
    phone = update.message.text
    user_id = update.message.chat_id
    user_name = update.message.from_user.first_name
    active_sessions[user_id]['phone']=phone
    message_content = '''
    Alright {0} I have your phone number {1}.

    What cca are you representing?
    '''
    bot.send_message(chat_id=update.message.chat_id,\
    text=message_content.format(user_name,str(phone)))
    return CCA

def newrequest_geteventname(bot, update):
    user_id = update.message.from_user.id
    cca = update.message.text
    active_sessions[user_id]['cca']=cca
    user_name = update.message.from_user.first_name
    message_content = '''
    Okay {0} from {1},

    What is the name of your event?
    '''
    bot.send_message(chat_id=update.message.chat_id, \
    text=message_content.format(user_name, cca))
    return EVENT

def newrequest_getvenue(bot, update):
    user_id = update.message.from_user.id
    event = update.message.text
    active_sessions[user_id]['event']=event
    user_name = update.message.from_user.first_name
    message_content = '''
    Where is {0} held?
    '''
    bot.send_message(chat_id=update.message.chat_id, \
    text=message_content.format(event))
    return VENUE

def newrequest_getdatetime(bot, update):
    user_id = update.message.from_user.id
    venue = update.message.text
    active_sessions[user_id]['venue']=venue
    user_name = update.message.from_user.first_name
    event = active_sessions[user_id]['event']
    message_content = '''
    {0} will be held at {1} on what date and time? Please include start and end time.

    eg 24 Sep, 7pm - 9pm
    '''
    bot.send_message(chat_id=update.message.chat_id, \
    text=message_content.format(event, venue))
    return DATETIME

def newrequest_getdescription(bot, update):
    user_id = update.message.from_user.id
    datetime = update.message.text
    active_sessions[user_id]['datetime'] = datetime
    user_name = update.message.from_user.first_name
    message_content = '''
    Tell me more about your event, {0}.

    What items do you have planned for your event?
    Will there be any performances?
    Do you plan to use the projector and screen?
    Do you have any special requests?

    Please be as descriptive as possible! The more details I have, the better I can assist you :)
    '''
    bot.send_message(chat_id=update.message.chat_id, \
    text=message_content.format(user_name))
    return DESCRIPTION

def newrequest_confirm(bot, update):
    description = update.message.text
    user_id = update.message.from_user.id
    active_sessions[user_id]['description']=description
    user_name = active_sessions[user_id]['name']
    cca = active_sessions[user_id]['cca']
    phone = active_sessions[user_id]['phone']
    event = active_sessions[user_id]['event']
    venue = active_sessions[user_id]['venue']
    datetime = active_sessions[user_id]['datetime']
    description = active_sessions[user_id]['description']
    message_content = '''
    Alright {0}, let me confirm a few things before submitting your request.

    Phone: {1}
    CCA: {2}
    Event Name: {3}
    Venue: {4}
    Date/Time: {5}
    Description:
    {6}

    Is this correct?
    '''.format(user_name, phone, cca, event, venue, datetime, description)
    message_id = update.message.message_id
    keyboard = [
        [InlineKeyboardButton('Yes', callback_data='yes.{}'.format(message_id)),\
        InlineKeyboardButton('No', callback_data='no.{}'.format(message_id))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.message.chat_id,\
    text=message_content, reply_markup=reply_markup)

def newrequest_finalise(bot, update):
    query = update.callback_query
    bot.edit_message_reply_markup(chat_id=query.message.chat_id,\
    message_id=query.message.message_id)
    response = query.data.split('.')
    user_id = query.from_user.id
    user_name = active_sessions[user_id]['name']
    if response[0] == 'yes':
        bot.send_message(chat_id=query.message.chat_id,\
        text="Ok, give me a moment...")
        #try send to dylan
        try:
            user_name = active_sessions[user_id]['name']
            cca = active_sessions[user_id]['cca']
            phone = active_sessions[user_id]['phone']
            event = active_sessions[user_id]['event']
            venue = active_sessions[user_id]['venue']
            datetime = active_sessions[user_id]['datetime']
            description = active_sessions[user_id]['description']
            message_content = '''
            New CMB request

            Name: {0}
            Phone: {1}
            CCA: {2}
            Event Name: {3}
            Venue: {4}
            Date/Time: {5}
            Description:
            {6}
            '''.format(user_name, phone, cca, event, venue, datetime, description)
            bot.send_message(chat_id=cmb_head, text=message_content)
        except:
            bot.send_message(chat_id=query.message.chat_id,\
            text='''
            Sorry {}, I have run into a problem placing your request.
            Can you try again using /newrequest?
            '''.format(user_name))
        else:
            bot.send_message(chat_id=query.message.chat_id,\
            text='''
            I have successfully placed your request, {}.
            I will contact you again soon to let you know if your request has been approved or rejected. Thank you!
            '''.format(user_name))
        finally:
            del active_sessions[user_id]
            return ConversationHandler.END
    elif response[0] == 'no':
        del active_sessions[user_id]
        bot.send_message(chat_id=query.message.chat_id,\
        text='''
        Alright {}, I have cancelled your request. If you wish to make a new request, you can simply type /newrequest again.
        See you soon!
        '''.format(user_name))
        return ConversationHandler.END
    else:
        bot.send_message(chat_id=query.message.chat_id,\
        text="I'm sorry, I don't understand what you mean. \
        Could we start again with /newrequest?")
        return ConversationHandler.END

def newrequest_cancel(bot, update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name
    del active_sessions[user_id]
    bot.send_message(chat_id=update.message.chat_id,\
    text='''
    Alright {}, I have cancelled your request. If you wish to make a new request, you can simply type /newrequest again.
    See you soon!
    '''.format(user_name))
    return ConversationHandler.END
