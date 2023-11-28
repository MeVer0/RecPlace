from dotenv import load_dotenv
import os

load_dotenv(r'C:\Users\Mever\OneDrive\Рабочий стол\RecPlace\.env.py')

secret = os.environ.get("SECRET")

# SMTP
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")
smtp_server = os.environ.get("SMTP_SERVER")
