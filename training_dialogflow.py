import os
import json
import logging
from dotenv import load_dotenv
from google.cloud import dialogflow

def read_json(file_json, encoding):
    with open(file_json, 'r', encoding=encoding) as questions:
        contents_json = questions.read()
    return json.loads(contents_json)
    

def create_intent(project_id, display_name, training_phrases_parts, message_texts):

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)        
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))

    
if __name__ == '__main__':
    logger = logging.getLogger(__file__)
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()    
    project_id = os.environ.get('PROJECT_ID')
    contents = read_json('training/questions.json', 'utf-8')
    
    for topic in contents:
        questions = contents[topic]['questions']  
        answer = contents[topic]['answer']
        if isinstance(answer, str):
            answer = [answer]
        create_intent(project_id, topic, questions, answer)
