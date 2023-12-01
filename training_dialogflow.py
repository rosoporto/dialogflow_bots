import os
import json
import logging
import argparse
from dotenv import load_dotenv
from google.cloud import dialogflow


logger = logging.getLogger(__file__)


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
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=logging_format, level=logging.INFO)
    
    load_dotenv()    
      
    parser = argparse.ArgumentParser(description='Training file for your bot')    
    parser.add_argument('training_file',
                        nargs='?',
                        help='File for training the bot in the json format',
                        default='questions.json')
    args = parser.parse_args()
    
    contents = read_json(args.training_file, 'utf-8')
    
    project_id = os.environ.get('PROJECT_ID')
        
    for topic, tasks in contents.items(): 
        questions = tasks['questions']
        answer = tasks['answer']
        if isinstance(answer, str):
            answer = [answer]
        print(project_id, topic, questions, answer)        
        create_intent(project_id, topic, questions, answer)
