from dotenv import load_dotenv, find_dotenv
from os import environ as env
from distutils.util import strtobool

def load_config_from_env(env_file=''):
    if env_file == '' or env_file == None:
        env_file = '.env'

    load_dotenv(find_dotenv(env_file))

    config = {
        'BAIDU_APP_ID': env.get("BAIDU_APP_ID"), 
        'BAIDU_API_KEY': env.get("BAIDU_API_KEY"),
        'BAIDU_SECRET_KEY': env.get("BAIDU_SECRET_KEY"),
        'PICOVOICE_API_KEY': env.get("PICOVOICE_API_KEY"),
        'OPENAI_API_ENDPOINT': env.get("OPENAI_API_ENDPOINT"),
        'OPENAI_API_KEY': env.get("OPENAI_API_KEY"),
        'OPENAI_API_PROMPT': env.get("OPENAI_API_PROMPT"),
        'PLAY_WELCOME_VOICE': eval(env.get("PLAY_WELCOME_VOICE")),
        'ENABLE_CHINESE_CORRECT': eval(env.get('ENABLE_CHINESE_CORRECT')),
        'ENABLE_SEMANTIC_ANALYSIS': eval(env.get('ENABLE_SEMANTIC_ANALYSIS')),
        'OPENWEATHERMAP_API_KEY': env.get("OPENWEATHERMAP_API_KEY"),
        'RASA_NLU_ENDPOINT': env.get("RASA_NLU_ENDPOINT"),
        'SHERPA_MODEL_PATH': env.get("SHERPA_MODEL_PATH")
    }

    return config


