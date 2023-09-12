import os
import vk_api as vk
import logging
import random
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger(__file__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main():
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    vk_group_token = os.environ.get('VK_GROUP_TOKEN')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)  


if __name__ == '__main__':
    main()
    