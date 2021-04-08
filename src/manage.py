from flask_migrate import MigrateCommand
from flask_script import Manager

from payments import app

manager = Manager(app.create_app)
manager.add_command('db', MigrateCommand)
ENVIRONMENTS = ['Development', 'Staging', 'Production']


@manager.command
def about():
    print("Receipts-service")


@manager.option('-u', dest='user', help='User name')
@manager.option('-e', dest='environment', choices=ENVIRONMENTS,
                help='Environment name [Development | Staging | Production]')
def generate_api_key(environment, user):
    import sys
    from itsdangerous import TimestampSigner
    from payments import config

    if environment not in ['Development', 'Staging', 'Production']:
        print('Invalid environment')
        sys.exit(1)

    config_env = getattr(config, '{0}Config'.format(environment))

    signer = TimestampSigner(config_env.SIGNER_KEY)
    print('APIKEY: {0}'.format(signer.sign(user)))


if __name__ == '__main__':
    manager.run()
