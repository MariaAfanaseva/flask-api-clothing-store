import os
from dotenv import load_dotenv

load_dotenv('configs/.env-users')

ADMIN_USER = {
    "email": os.getenv('ADMIN_EMAIL'),
    "password": os.getenv('ADMIN_PASSWORD'),
}

USER = {
    "email": os.getenv('USER_EMAIL'),
    "password": os.getenv('USER_PASSWORD'),
}
