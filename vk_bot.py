import os
import vk_api
import logging
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

logger = logging.getLogger(__file__)


def main():
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    vk_group_token = os.environ.get('VK_GROUP_TOKEN')

    vk_session = vk_api.VkApi(token=vk_group_token)

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()
    