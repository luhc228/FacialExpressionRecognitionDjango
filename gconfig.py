
from gevent import monkey
monkey.patch_all()
import multiprocessing
debug = True
chdir = '/home/rTeam/Desktop/Xu/FacialExpressionRecognitionDjango'
loglevel = 'debug'
bind = '0.0.0.0:5000'
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
workers = 4
worker_class = 'gevent' 
