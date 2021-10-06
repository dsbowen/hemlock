from hemlock import User, Page, create_app
from hemlock.questions import Label

Page.defaults["navbar"] = (
    "Brand",
    [
        "Current page",
        ("Route 0", "/route0"),
        ("Route 1", "/route1"),
        {"label": "Disabled", "disabled": True},
        (
            "Dropdown",
            [
                "Current page",
                ("Route 0", "/route0"),
                ("Route 1", "/route1"),
                {"label": "Disabled", "disabled": True},
            ],
        ),
    ],
)


@User.route("/route0")
def seed0():
    return Page(Label("Route 0."))


@User.route("/route1")
def seed1():
    return Page(Label("Route 1."))


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
