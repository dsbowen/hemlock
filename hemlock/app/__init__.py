"""Application factory, settings, statics, and templates"""

from hemlock.app.factory import create_app, db, gcp_client, gcp_bucket, socketio
from hemlock.app.settings import Settings