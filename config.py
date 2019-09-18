import os

class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 0
    SECRET_KEY = 'SoyUnaClaveSecreta'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'haroldesptru@gmail.com'
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
