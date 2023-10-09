import os
import time
import vk_api as vk
import logging
import random
import requests
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import detect_intent_texts
from tg_logs_handler import TgLogsHandler


logger = logging.getLogger(__file__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def vk_message(event, project_id, vk_api):
    answer_bot = detect_intent_texts(project_id,
                                    event.user_id,
                                    event.text)
    if not answer_bot.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer_bot.fulfillment_text,
            random_id=random.randint(1,1000))


def main():
    project = 'VK Bot'
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    vk_group_token = os.environ.get('VK_GROUP_TOKEN')
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    tg_bot_logger_token = os.environ.get('TG_BOT_LOGGER_TOKEN')    
    
    tg_handler = TgLogsHandler(tg_bot_logger_token, tg_chat_id)
    logger.addHandler(tg_handler)    
    
    logger.info(f'{project} started')
    
    while True:
        vk_session = vk.VkApi(token=vk_group_token)
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    vk_message(event, project_id, vk_api)                    
        except requests.exceptions.ReadTimeout:
            logger.error(f'{project}: Time Out')
            continue
        except requests.exceptions.ConnectionError:
            logger.error(f'{project}: Lost connection')
            time.sleep(600)


if __name__ == '__main__':
    main()
    