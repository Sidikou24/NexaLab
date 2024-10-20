import os

class Config:
    SECRET_KEY ='MY_Sqlite@KeyNexa2412'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sidikoudari@gmail.com'
    MAIL_PASSWORD = 'ckeq neaa slab viny'
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
 