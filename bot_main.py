TOKEN = "387409480:AAHmD7cUiq6-Hotji7_bxikR_mkoM0W7GjM"
dev_mode = True

from bot_commands import *
from telegram.ext import Updater
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', tutorial)
opensession_handler = CommandHandler('opensession', open_session)
endsession_handler = CommandHandler("endsession", end_session)
echo_handler = MessageHandler(Filters.text, echo)
whoami_handler = CommandHandler("whoami", whoami)
unknown_handler = MessageHandler(Filters.command, unknown)

newbooking_handler = CommandHandler('newbooking', newbooking)
checkstatus_handler = CommandHandler('checkstatus', workinprogress)
amend_handler = CommandHandler('amend', workinprogress)
cancel_handler = CommandHandler('cancel', workinprogress)
view_handler = CommandHandler('view', workinprogress)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(opensession_handler)
dispatcher.add_handler(endsession_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(whoami_handler)

dispatcher.add_handler(newbooking_handler)
dispatcher.add_handler(checkstatus_handler)
dispatcher.add_handler(amend_handler)
dispatcher.add_handler(cancel_handler)
dispatcher.add_handler(view_handler)

dispatcher.add_handler(unknown_handler)

### initialise bot ###
if dev_mode:
    print("Listening for new messages...")
updater.start_polling()
