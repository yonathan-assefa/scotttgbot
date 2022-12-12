# telegram bot accept zip file and forward it to the admin
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram import ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)
from dotenv import load_dotenv

import os

load_dotenv()

TOKEN = os.getenv('TOKEN')
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
ADMIN = os.getenv('ADMIN') 
ARCHIVE = os.getenv('ARCHIVE')
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context:CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}!")
    current_user = update.message.from_user
    # user profile photo stated using this bot 
    try:
        context.bot.send_photo(chat_id = ADMIN, photo = current_user.photo_url, caption = f"{current_user} +  started using this bot! \n\nPlease check it out!")
    except:
        context.bot.send_message(chat_id  = ADMIN, text = f"{current_user} \n started using this [CSECDev WeeklyChallenge Bot] bot! \n\nPlease check it out!")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Use this Bot to Submit Your Project Video \n\nFor CSECDev members only!\n\n\n #CSEC #CSECDev")


def echo(update: Update, context: CallbackContext) -> None:
    """Forward the user message."""
    # check if the file is video
    # if update.message.document.mime_type != 'video/mp4':
    #     update.message.reply_text("Please send a video file! llll")
    #     return
    # get current user id
    current_user = update.message.from_user
    
    # forward video to admin
    context.bot.send_message(chat_id  = ARCHIVE, text = f"New Project Video Submission! \n\nPlease check it out! from: \n{current_user}")
    context.bot.forward_message(chat_id = ARCHIVE, from_chat_id = update.message.chat_id, message_id = update.message.message_id)
    update.message.reply_text("Your Project Video has been submitted successfully ! \n\nThank you! \n\n\n #CSEC #CSECDev")

def error__message(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    current_user = update.message.from_user
    context.bot.forward_message(chat_id = ADMIN, from_chat_id = update.message.chat_id, message_id = update.message.message_id)
    context.bot.send_message(chat_id  = ADMIN, text = f"{current_user} +  sent a message that is not a video file! \n\nPlease check it out!")
    update.message.reply_text("Please send a video file only! \n\nThank you for your cooperation!\n\n\n #CSEC #CSECDev")


def main() -> None:
    """Start the bot."""
    updater = Updater(token = TOKEN,use_context = True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram


    # only accept video file and forward it to admin
    dispatcher.add_handler(MessageHandler(Filters.video & ~Filters.command, echo))
    # dispatcher.add_handler(MessageHandler(Filters.document.VIDEO & ~Filters.command, echo))
    # except video file and commands send error message
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.video & ~Filters.command, error__message))
    # Run the bot until the user presses Ctrl-C
    updater.start_polling()


if __name__ == "__main__":
    main()







