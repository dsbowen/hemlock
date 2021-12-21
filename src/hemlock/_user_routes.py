"""User routes.
"""
from __future__ import annotations

import copy
from typing import Tuple, Union
from urllib.parse import urlparse, parse_qs

from flask import current_app, request, url_for
from flask_login import current_user, login_required, logout_user
from werkzeug.wrappers import Response

from .app import bp, db, static_pages
from .page import Page
from .questions import Label
from .user import User
from .utils import redirect


@bp.route("/")
def index() -> Response:
    """Redirect the client.

    The client may be redirected to the screenout page, the restart page, or the first
    page of the study.

    Returns:
        Response: Redirect.
    """

    def matching_record_found(mapping):
        return any([value in mapping.get(key, []) for key, value in meta_data.items()])

    if "next" in request.args:
        # get querystring arguments from the redirect
        parsed_url = urlparse(request.args["next"])
        meta_data = dict(parse_qs(parsed_url.query))
        meta_data = {
            key: (value[0] if len(value) == 1 else value)
            for key, value in meta_data.items()
        }
        meta_data["next"] = parsed_url.path
    else:
        meta_data = dict(request.args)

    meta_data["ipv4"] = request.remote_addr  # type: ignore

    if matching_record_found(current_app.config["SCREENOUT_RECORDS"]):
        return redirect(url_for("hemlock.screenout"))

    if current_user.is_authenticated:
        if (
            current_user.get_tree().page.is_first_page
            or not current_app.config["ALLOW_USERS_TO_RESTART"]
        ):
            return redirect(User.default_url_rule)  # type: ignore
        return redirect(url_for("hemlock.restart"))

    if matching_record_found(user_metadata := current_app.config["USER_METADATA"]):
        return redirect(url_for("hemlock.screenout"))

    for key, value in meta_data.items():
        if key in current_app.config["BLOCK_DUPLICATE_KEYS"]:
            user_metadata[key].append(value)

    User(meta_data=meta_data)
    db.session.commit()
    return redirect(User.default_url_rule)  # type: ignore


@bp.route("/screenout")
def screenout() -> str:
    """Screenout page.

    Returns:
        str: Screenout page.
    """
    screenout_page_key = "screenout"
    if screenout_page_key not in static_pages:
        static_pages[screenout_page_key] = Page(
            Label(
                """
                Our records indicate that you have already participated in this or 
                similar surveys.
                
                Thank you for your continuing interest in our research!
                """
            ),
            navbar=None,
            back=False,
            forward=False,
        ).render()

    return static_pages[screenout_page_key]


@bp.route("/restart", methods=["GET", "POST"])
@login_required
def restart() -> Union[str, Response]:
    """Restart page.

    Returns:
        Union[str, Response]: Restart page or redirect to study.
    """
    if request.method == "POST":
        if request.form.get("direction") == "forward":
            meta_data = copy.deepcopy(current_user.meta_data)
            logout_user()
            User(meta_data=meta_data)
            db.session.commit()

        return redirect(User.default_url_rule)  # type: ignore

    restart_page_key = "restart"
    if restart_page_key not in static_pages:
        static_pages[restart_page_key] = Page(
            Label(
                """
                You have already started this survey. Click "Resume" to pick up where 
                you left off or "Restart" to start the survey from the beginning.

                If you restart the survey, your responses will not be saved.
                """
            ),
            back="Resume",
            forward="Restart",
        ).render()

    return static_pages[restart_page_key]


@bp.errorhandler(500)
def internal_server_error(error) -> Tuple[str, int]:
    """Handle internal server error."""
    current_user.errored = True
    db.session.commit()

    internal_server_error_page_key = "500"
    if internal_server_error_page_key not in static_pages:
        static_pages[internal_server_error_page_key] = Page(
            Label(
                """
                The application encountered an error. Please contact the survey 
                administrator.

                We apologize for the inconvenience and thank you for your patience as we 
                work to resolve this issue.
                """
            ),
            navbar=None,
            back=False,
            forward=False,
        ).render()

    return static_pages[internal_server_error_page_key], 500
