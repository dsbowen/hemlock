"""Admin routes.
"""
from __future__ import annotations

import csv
import io
from datetime import timedelta
from typing import Union

import pandas as pd
from flask import request, send_file, session, url_for, wrappers
from werkzeug.wrappers import Response

from .admin_route_utils import (
    PASSWORD_KEY,
    in_gitpod_ide,
    login_required,
    navbar,
    password_is_correct,
)
from .app import bp, db, static_pages
from .user import User
from .page import Page
from .questions import Input, Label
from .utils import redirect
from .utils.statics import pandas_to_html, recompile_at_interval


@bp.route("/admin-login", methods=["GET", "POST"])
def admin_login() -> Union[str, Response]:
    """Admin login page.

    Returns:
        Union[str, Response]: HTML of the login page or redirect to a page in the admin
            dashboard.
    """
    # truncate to 10 because the hash can be at most 10 characters long
    password_input_hash = "password_input_hash"[:10]
    login_page_hash_key = "login_page_id"
    default_url = "/admin-status"
    requested_url = request.args.get("requested_url")

    if request.method == "POST":
        # send the admin to the dashboard if the password was correct
        session[PASSWORD_KEY] = request.form[password_input_hash]
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
            navbar=navbar,
            back=False,
            forward="Login",
        )
        password_input.hash = password_input_hash
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


@bp.route("/admin-logout")
@login_required
def admin_logout() -> Response:
    """Clear the password cookie.

    Returns:
        Response: Redirect to login page.
    """
    session.clear()
    return redirect("/admin-login")


@bp.route("/admin-download")
@login_required
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
@login_required
def admin_status() -> str:
    """User status page.

    Returns:
        str: HTML.
    """
    init_label: str = "No users yet. Go get some people to take your survey!"
    if in_gitpod_ide():
        # websocket will not reliably connect in gitpod
        # but will work in VS code remote
        page = Page(
            label := Label(init_label), navbar=navbar, forward=False, back=False
        )
        get_user_status(label)
        return page.render()

    status_page_key = "status"
    if status_page_key not in static_pages:
        # create and cache user status page
        page = Page(
            recompile_at_interval(
                30000,
                label := Label(init_label, compile=get_user_status),
            ),
            navbar=navbar,
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
