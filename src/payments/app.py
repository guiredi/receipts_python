import logging.config
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimestampSigner

from payments.celery_config import celery
from payments.config import DevelopmentConfig, ProductionConfig, StagingConfig, TestingConfig

db = SQLAlchemy(session_options={'autoflush': False})


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')) -> Flask:
    app = Flask(__name__)
    CORS(app)
    configuration = {
        'Development': DevelopmentConfig,
        'Production': ProductionConfig,
        'Staging': StagingConfig,
        'Testing': TestingConfig
    }[config_var]
    app.config.from_object(configuration)

    # _register_bluprints(app)

    db.init_app(app)
    celery.init_app(app)

    Migrate(app, db)

    return app


# def _register_bluprints(app: Flask):
#     # app.register_blueprint(bp_common)
#     # v1.init_app(app)


def _configure_extensions(app: Flask):
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])
    app.signer = TimestampSigner(app.config['SIGNER_KEY'])


def create_celery_app():
    create_app()
    return celery


celery_app = create_celery_app()
