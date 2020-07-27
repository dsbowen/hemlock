"""Hemlock application file"""

# import survey
import tmp_survey2

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)