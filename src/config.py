import os

from dotenv import load_dotenv

load_dotenv(r'C:\Users\Mever\OneDrive\Рабочий стол\RecPlace\.env.py')

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_host = os.environ.get("DB_HOST")
db_name = os.environ.get("DB_NAME")