import flask
from celery import Celery
from kombu import Queue, Exchange


class FlaskCelery(Celery):

    def __init__(self, *args, **kwargs):

        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()
        self.app = None

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self._configure_backend()
        self.autodiscover_tasks(packages={"payments.service_layer.event_consumer"})

    def _configure_backend(self):
        if not self.app:
            raise Exception("Must call init_app first")

        process_credit_card_payment_queue = self.app.config[
            'QUEUE_PROCESS_CREDIT_CARD_PAYMENT']

        TASK_QUEUES = (
            Queue(process_credit_card_payment_queue,
                  Exchange(process_credit_card_payment_queue),
                  routing_key=process_credit_card_payment_queue),
        )
        confs = {
            'broker_url': self.app.config['BROKER_URL'],
            'task_queues': TASK_QUEUES,
            'broker_transport_options': self.app.config['BROKER_TRANSPORT_OPTIONS']
        }

        self.conf.update(**confs)


celery = FlaskCelery()
