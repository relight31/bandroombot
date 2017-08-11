TOKEN = "387409480:AAHmD7cUiq6-Hotji7_bxikR_mkoM0W7GjM"
dev_mode = True

from bot_commands import *
from telegram.ext import Updater
updater = Updater(token = TOKEN)
dispatcher = updater.dispatcher

from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram.ext import ConversationHandler

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', tutorial)
idk_handler = MessageHandler(Filters.text, idk)
whoami_handler = CommandHandler("whoami", whoami)
bigbrotherhandler = CommandHandler("togglebigbro", bigbrothertoggle)
unknown_handler = MessageHandler(Filters.command, unknown)

newbooking_handler = ConversationHandler(
    entry_points=[CommandHandler('newbooking',newbooking_start)],

    states={
        CCA: [CallbackQueryHandler(newbooking_gettime)],
        TIME: [MessageHandler(Filters.text, newbooking_getreason)],
        REASON: [MessageHandler(Filters.text, newbooking_confirm)]
    },
    fallbacks=[
        CallbackQueryHandler(newbooking_finalise),
        CommandHandler('cancel', newbooking_cancel)
    ]
)
checkstatus_handler = CommandHandler('checkstatus', workinprogress)
amend_handler = CommandHandler('amend', workinprogress)
cancel_handler = CommandHandler('cancel', workinprogress)
view_handler = ConversationHandler(
    entry_points=[CommandHandler('view', view_init)],

    states={
        VIEW_RESP: [CallbackQueryHandler(view_seebookings)]
    },
    fallbacks=[]
)
view_bookingresponse_handler = CallbackQueryHandler(view_bookingresponse)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(whoami_handler)
dispatcher.add_handler(bigbrotherhandler)

dispatcher.add_handler(newbooking_handler)
dispatcher.add_handler(checkstatus_handler)
dispatcher.add_handler(amend_handler)
dispatcher.add_handler(cancel_handler)
dispatcher.add_handler(view_handler)
dispatcher.add_handler(view_bookingresponse_handler)

dispatcher.add_handler(idk_handler)
dispatcher.add_handler(unknown_handler)

### initialise bot ###
if dev_mode:
    print("Listening for new messages...")
updater.start_polling()
