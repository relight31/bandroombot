TOKEN = "387409480:AAHmD7cUiq6-Hotji7_bxikR_mkoM0W7GjM"
dev_mode = False

from bot_commands import *
from telegram.ext import Updater
import os
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
unknown_handler = MessageHandler(Filters.command, unknown)

newrequest_handler = ConversationHandler(
    entry_points=[CommandHandler('newrequest',newrequest_start)],

    states={
        PHONE: [MessageHandler(Filters.text, newrequest_getcca)],
        CCA: [MessageHandler(Filters.text, newrequest_geteventname)],
        EVENT: [MessageHandler(Filters.text, newrequest_getvenue)],
        VENUE: [MessageHandler(Filters.text, newrequest_getdatetime)],
        DATETIME: [MessageHandler(Filters.text, newrequest_getdescription)],
        DESCRIPTION: [MessageHandler(Filters.text, newrequest_confirm)]
    },
    fallbacks=[
        CallbackQueryHandler(newrequest_finalise),
        CommandHandler('cancel', newrequest_cancel)
    ]
)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(whoami_handler)

dispatcher.add_handler(newrequest_handler)

dispatcher.add_handler(idk_handler)
dispatcher.add_handler(unknown_handler)

### initialise bot ###
print("Listening for new messages...")
if dev_mode:
    updater.start_polling()
else:
    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://kebandroombot.herokuapp.com/" + TOKEN)
updater.idle()
