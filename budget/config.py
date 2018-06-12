import os  # module that will allow for environment variables to be imported


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')  # environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')  # environment variable
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # environment variable
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # environment variable
