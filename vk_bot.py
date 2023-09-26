import os
import vk_api as vk
import logging
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType
from dialogflow import detect_intent_texts


logger = logging.getLogger(__file__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )
    
    
def vk_message(dialogflow_project_id, vk_group_token):
    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    
    try:            
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                answer_bot = detect_intent_texts(dialogflow_project_id,
                                                event.user_id,
                                                event.text)
                if not answer_bot.intent.is_fallback:
                    vk_api.messages.send(
                        user_id=event.user_id,
                        message=answer_bot.fulfillment_text,
                        random_id=random.randint(1,1000))
    except Exception as e:
        logger.exception(e)


def main():
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    project_id = os.environ.get('PROJECT_ID')
    vk_group_token = os.environ.get('VK_GROUP_TOKEN')
    
    vk_message(project_id, vk_group_token)


if __name__ == '__main__':
    main()
    