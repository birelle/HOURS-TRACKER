import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/hrs_tracker'
    SQLALCHEMY_TRACK_MODIFICATIONS = False