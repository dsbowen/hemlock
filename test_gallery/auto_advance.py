from hemlock import User, Page, create_app
from hemlock.functional import compile
from hemlock.questions import Label

@User.route("/survey")
def seed():
    return [
        Page(
            Label(
                "Remaining time: <span id='clock-id'></span>",
                compile=compile.auto_advance(10000, clock_id="clock-id")
            ),
        ),
        Page(
            Label("The End."),
        )
    ]

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)