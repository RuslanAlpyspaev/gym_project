from celery import Celery

app = Celery('second_service', broker='pyamqp://guest@rabbitmq//')

app.conf.update(
    result_backend='rpc://',
    task_routes={
        'second_service.tasks.add': 'low-priority',
    },
)


@app.task
def add(x, y):
    return x + y
