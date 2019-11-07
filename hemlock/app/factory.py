"""Application factory"""

from hemlock.app.extensions import Viewer
from hemlock.app.settings import get_settings, get_screenouts, Config

from datetime import datetime, timedelta
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_download_btn import DownloadBtnManager
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_worker import Manager
from redis import Redis
from rq import Queue
import eventlet

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
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
login_manager.login_message = None
scheduler = APScheduler()
eventlet.monkey_patch(socket=True)
socketio = SocketIO(async_mode='eventlet')
manager = Manager(db=db, socketio=socketio)
viewer = Viewer()

def create_app(settings):
    """Application factory
    
    First configure the application. Then initialize extensions.
    """
    settings, static, templates = get_settings(settings)
    app = Flask(__name__, static_folder=static, template_folder=templates)
    app.__dict__.update(settings)
    app.config.from_object(Config)
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = Queue('hemlock-task-queue', connection=app.redis)
    app.register_blueprint(bp)
    get_screenouts(app)
    
    bootstrap.init_app(app)
    db.init_app(app)
    download_btn_manager.init_app(app, **app.download_btn_settings)
    login_manager.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    socketio.init_app(app, message_queue=app.config['REDIS_URL'])
    manager.init_app(app, **app.manager_settings)
    viewer.init_app(app)
    
    return app