"""User routes.
"""
from __future__ import annotations

import copy
from typing import Union

from flask import current_app, redirect, request, url_for
from flask_login import current_user, login_required, logout_user
from werkzeug.wrappers import Response

from .app import bp, db
from .user import User


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

    meta_data = dict(request.args)
    meta_data["ipv4"] = request.remote_addr  # type: ignore

    if matching_record_found(current_app.settings["screenout_records"]):  # type: ignore
        return redirect(url_for("hemlock.screenout"))

    if current_user.is_authenticated:
        if (
            current_user.get_tree().page.is_first_page
            or not current_app.settings["allow_users_to_restart"]  # type: ignore
        ):
            return redirect(User.default_url_rule)  # type: ignore
        return redirect(url_for("hemlock.restart"))

    if matching_record_found(current_app.user_metadata):  # type: ignore
        return redirect(url_for("hemlock.screenout"))

    for key, value in meta_data.items():
        if key in current_app.settings["block_duplicate_keys"]:  # type: ignore
            current_app.user_metadata[key].append(value)  # type: ignore

    User(meta_data=meta_data)
    db.session.commit()
    return redirect(User.default_url_rule)  # type: ignore


@bp.route("/screenout")
def screenout() -> str:
    """Screenout page.

    Returns:
        str: Screenout page.
    """
    return current_app.settings["screenout_page"]  # type: ignore


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

    return current_app.settings["restart_page"]  # type: ignore


@bp.errorhandler(500)
def internal_server_error(error):
    current_user.errored = True
    db.session.commit()
    return current_app.settings["internal_server_error_page"], 500
