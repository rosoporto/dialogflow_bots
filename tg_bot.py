import os
import time
import logging
from dotenv import load_dotenv
from functools import partial
from dialogflow import detect_intent_texts
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext
)
from tg_logs_handler import TgLogsHandler


logger = logging.getLogger(__file__)


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте")
  
        
def echo(update, context, project_id, tg_chat_id):    
    answer = detect_intent_texts(project_id, tg_chat_id,
                                update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id,
                                text=answer.fulfillment_text)

    
def send_error(update: Update, context: CallbackContext) -> None:
    logger.error(msg='Возникло исключение при обработке сообщения:',
                exc_info=context.error)
    if update.effective_message:
        text = 'Произошла ошибка в момент обработки сообщения. ' \
               'Мы уже работаем над этой проблемой.'
        context.bot.send_message(chat_id=update.effective_chat.id,
                                text=text)


def main():
    project = 'TG Bot'
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)    
    
    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    tg_bot_logger_token = os.environ.get('TG_BOT_LOGGER_TOKEN')    
    
    tg_handler = TgLogsHandler(tg_bot_logger_token, tg_chat_id)
    logger.addHandler(tg_handler)
    
    callback_echo = partial(echo,
                            project_id=project_id,
                            tg_chat_id=tg_chat_id)
     
    logger.info(f'{project} started')    
    while True:
        try:
            updater = Updater(token=tg_bot_token)
            dispatcher = updater.dispatcher
            
            start_handler = CommandHandler('start', start)
            dispatcher.add_handler(start_handler)
            
            echo_handler = MessageHandler(Filters.text & (~Filters.command),
                                          callback_echo)
            dispatcher.add_handler(echo_handler)
            
            dispatcher.add_error_handler(send_error)
            
            updater.start_polling()
            updater.idle()
        except Exception as exc:
            logger.exception(exc)
            time.sleep(60)

if __name__ == '__main__':
    main()
    