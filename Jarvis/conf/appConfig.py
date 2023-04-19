from dotenv import load_dotenv, find_dotenv
from os import environ as env

def load_config_from_env(env_file=''):
    if env_file == '' or env_file == None:
        env_file = '.env'

    load_dotenv(find_dotenv(env_file))

    config = {
        'BAIDU_ASR_APP_ID': env.get("BAIDU_ASR_APP_ID"), 
        'BAIDU_ASR_API_KEY': env.get("BAIDU_ASR_API_KEY"),
        'BAIDU_ASR_SECRET_KEY': env.get("BAIDU_ASR_SECRET_KEY"),
        'PICOVOICE_API_KEY': env.get("PICOVOICE_API_KEY"),
        'OPENAI_API_ENDPOINT': env.get("OPENAI_API_ENDPOINT"),
        'OPENAI_API_KEY': env.get("OPENAI_API_KEY"),
        'OPENAI_API_PROMPT': env.get("OPENAI_API_PROMPT"),
        'PLAY_WELCOME_VOICE': bool(env.get("PLAY_WELCOME_VOICE")),
        'ENABLE_CHINESE_CORRECT': bool(env.get('ENABLE_CHINESE_CORRECT')),
        'ENABLE_SEMANTIC_ANALYSIS': bool(env.get('ENABLE_SEMANTIC_ANALYSIS'))
    }

    return config


