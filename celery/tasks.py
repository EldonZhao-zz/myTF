from celery import Celery
import time


app = Celery('tasks', broker='amqp://guest@localhost//', backend='amqp://guest@localhost//')


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x):
    result = 0
    for i in xrange(x):
        time.sleep(x)
        result += i
    return result
