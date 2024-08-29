from celery import Celery

celery_app = Celery(
    'worker',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
    include=['app.api.crud']
)

celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
