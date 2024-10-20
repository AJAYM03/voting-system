# config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'  # Replace with a strong default secret key
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'root'        # Replace with your MySQL username
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'sarangpallom'  # Replace with your MySQL password
    DB_NAME = os.environ.get('DB_NAME') or 'voting_system'          # Replace with your MySQL database name
