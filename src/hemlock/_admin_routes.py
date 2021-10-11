"""Admin routes.
"""
from __future__ import annotations

import csv
import io
from datetime import timedelta
from functools import wraps
from typing import Callable, Union

import pandas as pd
from flask import current_app, redirect, request, send_file, session, url_for, wrappers
from werkzeug.wrappers import Response
from werkzeug.security import check_password_hash

from .app import bp, db, static_pages
from .user import User
from .page import Page
from .questions import Input, Label
from .utils.statics import pandas_to_html, recompile_at_interval

PASSWORD_KEY = "admin_password"

admin_navbar = (
    (
        """
        <img src="https://dsbowen.gitlab.io/hemlock/_static/banner.png" style="max-height:30px;" alt="Hemlock">
        """,
        "https://dsbowen.gitlab.io/hemlock"
    ),
    [
        ("User status", "/admin-status"),
        ("Download", "/admin-download"),
        ("Logout", "/admin-logout"),
    ],
)


@bp.route("/admin-login", methods=["GET", "POST"])
def admin_login() -> Union[str, Response]:
    """Admin login page.

    Returns:
        Union[str, Response]: HTML of the login page or redirect to a page in the admin
            dashboard.
    """
    login_page_hash_key = "login_page_id"
    default_url = "/admin-status"
    requested_url = request.args.get("requested_url")

    if request.method == "POST":
        # send the admin to the dashboard if the password was correct
        session[PASSWORD_KEY] = next(request.form.values())
        if password_is_correct():
            return redirect(requested_url or default_url)
        return redirect(url_for("hemlock.admin_login", requested_url=requested_url))

    # get the admin login page
    page = None
    if login_page_hash_key in session:
        page = Page.query.filter_by(hash=session[login_page_hash_key]).first()

    if page is None:
        # create an admin login page for this session
        page = Page(
            password_input := Input(
                "Enter your password.",
                floating_label="Password",
                input_tag={"type": "password"},
            ),
            navbar=admin_navbar,
            back=False,
            forward="Login",
        )
        db.session.add(page)
        db.session.commit()
        session[login_page_hash_key] = page.hash
    else:
        password_input = page.questions[0]

    if not password_is_correct():
        # add error message if password was incorrect
        if PASSWORD_KEY in session or requested_url is not None:
            password_input.set_is_valid(False)
            if PASSWORD_KEY in session:
                password_input.feedback = "Incorrect password."
            else:
                password_input.feedback = "Password required."

    db.session.commit()
    return page.render()


def password_is_correct() -> bool:
    """Checks if the client has the correct password stored in session.

    Returns:
        bool: Correct password indicator.
    """
    return check_password_hash(
        current_app.config.get("PASSWORD_HASH"),  # type: ignore
        session.get(PASSWORD_KEY, ""),
    )


def admin_login_required(
    view_function: Callable[[], Union[str, Response]]
) -> Callable[[], Union[str, Response]]:
    """Decorator requiring admin login before accessing a page.

    Args:
        view_function (Callable[[], Union[str, Response]]): Admin view function.

    Returns:
        Callable[[], Union[str, Response]]: Decorated view function.
    """

    @wraps(view_function)
    def login_required_wrapper():
        if password_is_correct():
            return view_function()

        requested_url = url_for(f"hemlock.{view_function.__name__}")
        return redirect(url_for("hemlock.admin_login", requested_url=requested_url))

    return login_required_wrapper


@bp.route("/admin-logout")
@admin_login_required
def admin_logout() -> Response:
    """Clear the password cookie.

    Returns:
        Response: Redirect to login page.
    """
    session.clear()
    return redirect("/admin-login")


@bp.route("/admin-download")
@admin_login_required
def admin_download() -> wrappers.Response:
    """Download the users' data.

    Returns:
        wrappers.Response: CSV of the users' data.
    """
    df = User.get_all_data(to_pandas=False)
    writer = csv.writer(stringio := io.StringIO())
    writer.writerow(df.keys())
    writer.writerows(zip(*df.values()))

    bytesio = io.BytesIO()
    bytesio.write(stringio.getvalue().encode())
    bytesio.seek(0)
    stringio.close()

    return send_file(
        bytesio, as_attachment=True, download_name="data.csv", mimetype="text/csv"
    )


@bp.route("/admin-status")
@admin_login_required
def admin_status() -> str:
    """User status page.

    Returns:
        str: HTML.
    """
    status_page_key = "status"
    if status_page_key not in static_pages:
        # create and cache user status page
        page = Page(
            recompile_at_interval(
                30000,
                label := Label(
                    "No users yet. Go get some people to take your survey!",
                    compile=get_user_status,
                ),
            ),
            navbar=admin_navbar,
            forward=False,
            back=False,
        )
        db.session.add(label)
        db.session.commit()
        static_pages[status_page_key] = page.render()

    return static_pages[status_page_key]


def get_user_status(status_label: Label) -> None:
    """Get the user status label.

    Contains information about the number of users, their status, and time spent on
    the study.

    Args:
        status_label (Label): User status label.
    """
    meta_df = pd.DataFrame([user.get_meta_data() for user in User.query.all()])
    if len(meta_df) == 0:
        return

    # count users by status
    status_df = meta_df[["completed", "failed", "errored", "in_progress"]].sum()
    status_df["all"] = len(meta_df)
    status_df = status_df.to_frame("Count")

    # get median time by status
    median_time = [
        meta_df[meta_df[column]].total_seconds.quantile(0.5)
        for column in ("completed", "failed", "errored", "in_progress")
    ]
    median_time.append(meta_df.total_seconds.quantile(0.5))
    status_df["Median time"] = median_time
    status_df["Median time"] = status_df["Median time"].apply(
        lambda x: None if pd.isna(x) else str(timedelta(seconds=int(x)))
    )

    status_label.label = pandas_to_html(status_df)
