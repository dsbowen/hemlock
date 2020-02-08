"""Application factory"""

from hemlock.app.settings import Config, Settings, get_app_settings, get_screenouts

from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_download_btn import DownloadBtnManager
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_worker import Manager
from google.cloud import storage
from redis import Redis
from rq import Queue
import eventlet

from datetime import datetime, timedelta
import os

"""Extensions and blueprint registration"""
bootstrap = Bootstrap()
bp = Blueprint(
    'hemlock', 
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/hemlock/static'
)
db = SQLAlchemy()
download_btn_manager = DownloadBtnManager(db=db)
bucket = os.environ.get('BUCKET')
if bucket is not None:
    gcp_client = storage.Client()
    gcp_bucket = gcp_client.get_bucket(bucket)
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
login_manager.login_message = None
scheduler = APScheduler()
eventlet.monkey_patch(socket=True)
socketio = SocketIO(async_mode='eventlet')
manager = Manager(db=db, socketio=socketio)

def create_app():
    """Application factory
    
    First configure the application. Then initialize extensions.
    """
    app_settings, static, templates = get_app_settings()
    app = Flask(__name__, static_folder=static, template_folder=templates)
    app.__dict__.update(app_settings)
    app.config.from_object(Config)
    app.register_blueprint(bp)
    get_screenouts(app)

    if bucket is not None:
        app.gcp_client, app.gcp_bucket = gcp_client, gcp_bucket
    else:
        app.gcp_client = app.gcp_bucket = None

    redis_url = os.environ.get('REDIS_URL')
    if redis_url is not None:
        app.redis = Redis.from_url(redis_url)
        app.task_queue = Queue('hemlock-task-queue', connection=app.redis)
    else:
        app.redis = app.task_queue = None
    
    bootstrap.init_app(app)
    db.init_app(app)
    download_btn_manager.init_app(app, **Settings.get('download_btn_manager'))
    login_manager.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    socketio.init_app(app, message_queue=redis_url)
    manager.init_app(app, **Settings.get('manager'))
    
    return app