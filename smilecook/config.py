""" Configuration Data for the database"""
from os import getenv
from dotenv import load_dotenv

load_dotenv()

USER_NAME = getenv("USER_NAME")
PASSWORD = getenv("PASSWORD")
HOSTNAME = getenv("HOSTNAME")
DBNAME = getenv("DBNAME")
SECRET_KEY = getenv("SECRET_KEY")
JWT_ERROR_MESSAGE_KEY = getenv("JWT_ERROR_MESSAGE_KEY")
MAILGUN_DOMAIN = getenv("MAILGUN_DOMAIN")
MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")


class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{USER_NAME}:{PASSWORD}@{HOSTNAME}/{DBNAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = SECRET_KEY
    JWT_ERROR_MESSAGE_KEY = JWT_ERROR_MESSAGE_KEY
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    MAILGUN_DOMAIN = MAILGUN_DOMAIN
    MAILGUN_API_KEY = MAILGUN_API_KEY
    UPLOADED_IMAGES_DEST = "static/images"
    MAX_CONTENT_LENGTH = 10 * 1000 * 1000
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 10 * 60
    RATELIMIT_HEADERS_ENABLED = True
