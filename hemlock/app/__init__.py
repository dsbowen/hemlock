"""# Application factory and settings"""

import eventlet
eventlet.monkey_patch(socket=True)

from .settings import settings

import pandas as pd
from flask import Flask, Blueprint
# from flask_apscheduler import APScheduler
from flask_download_btn import DownloadBtnManager
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_worker import Manager
from sqlalchemy_mutable import MutableManager

import os

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
    from google.cloud import storage
    gcp_client = storage.Client()
    gcp_bucket = gcp_client.get_bucket(bucket)
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
login_manager.login_message = None
# scheduler = APScheduler()
socketio = SocketIO(async_mode='eventlet')
manager = Manager(db=db, socketio=socketio)
MutableManager.db = db
talisman = Talisman()

def push_app_context():
    """
    Push an app context for debugging in shell or notebook.

    Returns
    -------
    app : flask.app.Flask

    Examples
    --------
    ```python
    from hemlock import push_app_context

    app = push_app_context()
    ```

    Out:

    ```
    <Flask 'hemlock.app'>
    ```
    """
    from ..models.private import DataStore
    
    app = create_app()
    app.app_context().push()
    app.test_request_context().push()
    db.create_all()
    if not DataStore.query.first():
        db.session.add(DataStore())
        db.session.commit()
    return app

def create_app(settings=settings):
    """
    Create a Hemlock application.

    Parameters
    ----------
    settings : dict
        Default settings for the application, extensions, and models.

    Returns
    -------
    app : flask.app.Flask

    Examples
    --------
    In this example, we add a back button to every page in our survey.

    ```python
    from hemlock import Page, create_app, settings

    settings['Page'].update({'back': True})

    app = create_app()
    app.app_context().push()
    Page().preview()
    ```
    """
    app = _create_app(settings)
    _set_bucket(app)
    _set_redis(app)
    _init_extensions(app, settings)
    app.tmpfiles = []   
    return app

def _create_app(settings):
    app = Flask(
        __name__, 
        static_folder=settings.get('static_folder'), 
        template_folder=settings.get('template_folder'),
    )
    # get screenouts
    screenout_csv = settings.get('screenout_csv')
    if os.path.exists(screenout_csv):
        df = pd.read_csv(screenout_csv)
        screenout_keys = settings.get('screenout_keys')
        df = df[screenout_keys] if screenout_keys else df
        app.screenouts = df.to_dict(orient='list')
    else:
        app.screenouts = {}
    # store configuration, settings, and blueprint
    app.config.update(settings.get('Config'))
    app.settings = settings
    app.register_blueprint(bp)
    return app

def _set_bucket(app):
    """Set up google bucket"""
    if bucket is not None:
        app.gcp_client, app.gcp_bucket = gcp_client, gcp_bucket
    else:
        app.gcp_client = app.gcp_bucket = None

def _set_redis(app):
    """Set up Redis Queue"""
    redis_url = app.config.get('REDIS_URL')
    if redis_url is not None:
        from redis import Redis
        from rq import Queue
        app.redis = Redis.from_url(redis_url)
        app.task_queue = Queue('hemlock-task-queue', connection=app.redis)
    else:
        app.redis = app.task_queue = None

def _init_extensions(app, settings):
    """Initialize application extensions"""
    db.init_app(app)
    download_btn_manager.init_app(app, **settings.get('DownloadBtnManager'))
    login_manager.init_app(app)
    # scheduler.init_app(app)
    # scheduler.start()
    socketio.init_app(app, message_queue=app.config.get('REDIS_URL'))
    manager.init_app(app, **settings.get('Manager'))
    talisman.init_app(app, **settings.get('Talisman'))