import re
from pathlib import Path
import pickle
import openai
from unidecode import unidecode
from app.utils import logger
from app.utils.error_handler import custom_error_handler

CHAT_FOLDER = Path(__file__).parent.parent.parent / 'chat'
CHAT_FOLDER.mkdir(exist_ok=True)
CONFIG_FOLDER = CHAT_FOLDER / 'config'
CONFIG_FOLDER.mkdir(exist_ok=True)
MESSAGES_FOLDER = CHAT_FOLDER / 'messages'
MESSAGES_FOLDER.mkdir(exist_ok=True)
CACHE_DECONVERT = {}

def get_model_response(messages,
                            openai_key,
                            model='gpt-3.5-turbo',
                            temperature=0,
                            stream=False):
    logger.log_info(f"Connecting OpenAI API using model: {model}")
    try:
        # Set the OpenAI API key
        openai.api_key = openai_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )
        return response
    except Exception as e:
        # Handle the error using the custom error handler
        msg = 'Error connecting to OpenAI API'
        logger.log_error(f"{msg}: {e}")
        # Display the error message to the user
        
        # Log the error
        custom_error_handler(e)
        return None


def convert_message_name(message_name):
    file_name = unidecode(message_name)
    file_name = re.sub('\W+', '', file_name).lower()
    return file_name

def deconvert_message_name(file_name):
    if file_name not in CACHE_DECONVERT:
        message_name = read_message_by_file_name(file_name, key='message_name')
        CACHE_DECONVERT[file_name] = message_name
    return CACHE_DECONVERT[file_name]

def get_message_name(messages):
    message_name = ''
    for message in messages:
        if message['role'] == 'user':
            message_name = message['content'][:30]
            break
    return message_name

def save_messages(messages):
    if len(messages) == 0:
        return False
    message_name = get_message_name(messages)
    file_name = convert_message_name(message_name)
    file_to_save = {'message_name': message_name,
                    'file_name': file_name,
                    'message': messages}
    with open(MESSAGES_FOLDER / file_name, 'wb') as f:
        pickle.dump(file_to_save, f)

def read_message_by_file_name(file_name, key='message'):
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def read_messages(messages, key='message'):
    if len(messages) == 0:
        return []
    message_name = get_message_name(messages)
    file_name = convert_message_name(message_name)
    with open(MESSAGES_FOLDER / file_name, 'rb') as f:
        messages = pickle.load(f)
    return messages[key]

def list_conversations():
    conversations = list(MESSAGES_FOLDER.glob('*'))
    conversations = sorted(conversations, key=lambda item: item.stat().st_mtime_ns, reverse=True)
    return [c.stem for c in conversations]

# SAVING AND READING THE API KEY ========================

def save_key(key):
    with open(CONFIG_FOLDER / 'key', 'wb') as f:
        pickle.dump(key, f)

def read_key():
    if (CONFIG_FOLDER / 'key').exists():
        with open(CONFIG_FOLDER / 'key', 'rb') as f:
            return pickle.load(f)
    else:
        return ''
