import os
import logging
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters
)
from dialogflow import detect_intent_texts


logger = logging.getLogger(__file__)


def main():
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    project_id = os.environ.get('PROJECT_ID')
    
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")
        
    def echo(update, context):
        answer = detect_intent_texts(project_id, tg_chat_id, update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=answer.fulfillment_text)
    
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
    