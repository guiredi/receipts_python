import logging
import os

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    DEBUG = False
    TESTING = False

    LOGS_LEVEL = logging.INFO
    SIGNER_KEY = os.environ.get('SIGNER_KEY', 'S6210FFrsmQ6g7KBj6Au')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BROKER_URL = os.environ.get('BROKER_URL', '')
    BROKER_TRANSPORT_OPTIONS = os.environ.get('BROKER_TRANSPORT_OPTIONS', '{}')
    QUEUE_PROCESS_CREDIT_CARD_PAYMENT = os.environ.get('QUEUE_PROCESS_CREDIT_CARD_PAYMENT', '')


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_POOL_SIZE = None  # Avoids problems with SQLite


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    PRODUCTION = True


class StagingConfig(BaseConfig):
    pass
