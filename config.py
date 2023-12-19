import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config:
    # For encrytion
    SECRET_KEY = os.environ.get("SECRET_KEY") or "the-best-key"

    # For database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")

    # For languages
    LANGUAGES = ["en"]

    # For email server
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["admin_mail@example.com"]

    # Pagination
    POSTS_PER_PAGE = 3

    # Azure translation
    MS_TRANSLATOR_KEY = os.environ.get("MS_TRANSLATOR_KEY")
