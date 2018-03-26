from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import logging
import os
import sys
import subprocess

from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

from functools import wraps

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

#logging.basicConfig(filename="log_puerta.txt",
#                    filemode='a',
#                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                    datefmt='%H:%M:%S',
#                    level=logging.DEBUG)



logger = logging.getLogger(__name__)

door = port.PA6
gpio.init()
gpio.setcfg(door, gpio.OUTPUT)
gpio.output(door, 1)

# restrict access to some users
# please, include your chat_id here to interact with your bot
# example: 
# LIST_OF_ADMINS = [7237234,2423443,3423423]

LIST_OF_ADMINS = []

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            update.message.reply_text('You are not allowed to open my door!!')
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

@restricted
def press(bot, update):
    update.message.reply_text('Open/Close')
    gpio.output(door, 0)
    sleep(1)
    gpio.output(door, 1)
    logger.info("Someone opened the door")

def build_menu(bot, update):
    button_list = [
    ["/press"]
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list, resize_keyboard=True)
    update.message.reply_text('use /press to open/close the door', reply_markup=reply_markup)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Run bot."""
    # your bot token here
    # fake example: updater = Updater("300349534545JJK·453453453453:·45")
    updater = Updater("_your_token_from_botfather_")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher


    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("press", press))
    dp.add_handler(MessageHandler(Filters.text, build_menu))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=5)

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


