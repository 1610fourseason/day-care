import os


class BaseConfig:

    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')


    # Instagram Graph API
    INSTAGRAM_MAIN_URL = "https://graph.facebook.com"
    INSTAGRAM_VERSION = os.getenv("INSTAGRAM_VERSION", "v23.0")
    INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
    INSTAGRAM_PAGE_ID = os.getenv("INSTAGRAM_PAGE_ID")
    INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
    # threds API
    THREADS_MAIN_URL = "https://graph.threads.net"
    THREADS_VERSION = os.getenv("THREADS_VERSION", "v1.0")
    THREADS_ACCESS_TOKEN = os.getenv("THREADS_ACCESS_TOKEN")
    THREADS_USER_ID = os.getenv("THREADS_USER_ID")


class LocalConfig(BaseConfig):
    DEBUG = True

    # ngrok用エントリーポイント
    PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL')

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    DEBUG = False
    # ローカルテスト時はコメントアウトにする
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql+psycopg://')
    PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL')