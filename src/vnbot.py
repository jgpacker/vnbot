#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, filters

from bot_globals import *

from vndb import VNDB

import json

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=LOGGING_LEVEL)

logger = logging.getLogger(__name__)

vndb = VNDB()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')

def vn_search(bot, update):
    search_term = update.message.text
    result = vndb.search(search_term, flags="basic")
    response = map(lambda it: it['title'], json.loads(result))
    bot.sendMessage(update.message.chat_id, text=response)

def help(bot, update):
    HELP_TEXT='''
Send /vn-search <search-term> to get a list of search results from Vndb.org;
'''
    bot.sendMessage(update.message.chat_id, text=HELP_TEXT)

def ping(bot, update):
    bot.sendMessage(update.message.chat_id, text='pong')

def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))

def main():
    print 'start'
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(BOT_TOKEN)
    print 'updated'

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    print 'get dispatcher'

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))
    dp.addHandler(CommandHandler("vn-search", vn_search))
    print 'add handlers'

    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([filters.TEXT], echo))
    print 'message handler'

    # log all errors
    dp.addErrorHandler(error)
    print 'add error'

    # Start the Bot
    updater.start_polling()
    print 'polling'

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
