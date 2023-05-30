""" Configuration Data for the database"""


class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:deep@localhost/smilecook"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
