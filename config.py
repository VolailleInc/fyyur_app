import os

SECRET_KEY = os.urandom(38)

# Gets the folder within which the script is
basedir = os.path.abspath(os.path.dirname(__file__))

# Set debug mode active
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/fyyur'

# remove console warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
