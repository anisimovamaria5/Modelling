"""Модуль создания логгера"""
from atexit import register
from collections import defaultdict
import logging
from contextlib import contextmanager
from logging.handlers import TimedRotatingFileHandler
import os
from logging.handlers import QueueHandler, QueueListener
from multiprocessing import Queue
import time

class StatsHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.stats = defaultdict(int)
    
    def emit(self, record):
        self.stats[record.funcName] += 1

        
def set_logger():
    with open('DKS_math/logger/logs/app.csv', 'w') as f:
          f.write('name\tduration\n')

    logger = logging.getLogger(name='my_app')
    logger.setLevel(level='INFO')

    file_handler = logging.FileHandler('DKS_math/logger/logs/app.csv')
    
    formatter = logging.Formatter(
        '%(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

# logger = set_logger()

def setup_logging():
    with open('DKS_math/logger/logs/app.csv', 'w') as f:
        f.write('name\tduration\n')

    log_queue = Queue()
    formatter = logging.Formatter(
        '%(message)s'
    )
    file_handler = logging.FileHandler('DKS_math/logger/logs/app.csv')
    file_handler.setFormatter(formatter)

    queue_listener = QueueListener(log_queue, file_handler)
    queue_listener.daemon = True
    queue_listener.start()

    logger = logging.getLogger()
    logger.setLevel(level='INFO')
    logger.addHandler(QueueHandler(log_queue))
    return logger, queue_listener

logger, listener = setup_logging()

@contextmanager
def logging_context():
    try:
        yield
    finally:
        listener.stop()

