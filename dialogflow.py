import os
import sys
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)    
    text_input = dialogflow.TextInput(text=text, language_code='ru-ru')
    query_input = dialogflow.QueryInput(text=text_input)    
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


if __name__ == '__main__':
    logger = logging.getLogger(__file__)
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()
    tg_chat_id = os.environ.get('TG_CHAT_ID')
    project_id = os.environ.get('PROJECT_ID')
    text = sys.argv[1]
    answer = detect_intent_texts(project_id, tg_chat_id, text)
    print(answer.fulfillment_text)
