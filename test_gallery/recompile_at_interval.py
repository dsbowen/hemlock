"""Note that this simple clock application is more appropriate for pure
javascript/jquery. recompile_at_interval is more appropriate when you need to interact 
with the database.
"""
from datetime import datetime

from hemlock import User, Page, create_app, socketio
from hemlock.questions import Label
from hemlock.utils.statics import recompile_at_interval


@User.route("/survey")
def seed():
    return Page(
        recompile_at_interval(
            1000,  # update the time every second
            Label(compile=update_time)
        )
    )


def update_time(time_label):
    time_label.label = datetime.utcnow().strftime("%H:%M:%S")


app = create_app()

if __name__ == "__main__":
    socketio.run(app)