import requests
import cryptocompare
import time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


pricetomint = 0

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def gastomint(update,context):
    update.message.reply_text('Checking gas prices...\n')
    response = requests.get("https://ethgasstation.info/api/ethgasAPI.json?api-key=514b4fd9c00f25a8635d086783692ec1bedab91858475ea3203622c0d308")
    safelow = response.json()['safeLow']/10
    average = response.json()['average']/10
    fast = response.json()['fast']/10
    fastest = response.json()['fastest']/10

	#print("safe low: " + str(response.json()['safeLow']/10) + "\naverage:  " + str(response.json()['average']/10) + "\nfast:     " + str(response.json()['fast']/10)
	#+ "\nfastest:  " + str(response.json()['fastest']/10))

    ethprice = cryptocompare.get_price('ETH',curr='USD')['ETH']['USD']
    averageprice = (fast + fastest)/2
    avgpricetomint = (averageprice*10**(-9) * 241413)*ethprice
    avgpriceopenstore = (averageprice*10**(-9) * 3377029)*ethprice


    update.message.reply_text('Approximate average speed prices right now for Mintbase:'
    + '\nmint: ' +  str(round(avgpricetomint,2)) + ' USD' +
    '\nopen store: ' + str(round(avgpriceopenstore,2)) + ' USD')


def slowgastomint(update,context):
    update.message.reply_text('Checking gas prices...\n')
    response = requests.get("https://ethgasstation.info/api/ethgasAPI.json?api-key=514b4fd9c00f25a8635d086783692ec1bedab91858475ea3203622c0d308")

    safelow = response.json()['safeLow']/10
    average = response.json()['average']/10
    fast = response.json()['fast']/10
    fastest = response.json()['fastest']/10

	#print("safe low: " + str(response.json()['safeLow']/10) + "\naverage:  " + str(response.json()['average']/10) + "\nfast:     " + str(response.json()['fast']/10)
	#+ "\nfastest:  " + str(response.json()['fastest']/10))

    ethprice = cryptocompare.get_price('ETH',curr='USD')['ETH']['USD']
    averageprice = (fast + fastest)/2
    slowpricetomint = (safelow*10**(-9) * 241413)*ethprice
    avgpricetomint = (averageprice*10**(-9) * 241413)*ethprice
    slowpriceopenstore = (safelow*10**(-9) * 3377029)*ethprice
    avgpriceopenstore = (averageprice*10**(-9) * 3377029)*ethprice


    update.message.reply_text('Approximate slow speed prices right now for Mintbase:\nslow mint: ' +  str(round(slowpricetomint,2)) + ' USD'
    '\nslow open store: ' + str(round(slowpriceopenstore,2)) + ' USD')



def note(update, context):
   update.message.reply_text('Type /gastomint or /gastomintslow to see gas prices.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1593902712:AAFKsYk6-CZRF_-IoSB_dwed7QnoY3_ebHY", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("gastomint", gastomint))
    dp.add_handler(CommandHandler("gastomintslow", slowgastomint))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, note))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()



if __name__ == '__main__':
    main()
