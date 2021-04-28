"""Hemlock application file"""

import eventlet
eventlet.monkey_patch()

import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, host='0.0.0.0', debug=True)