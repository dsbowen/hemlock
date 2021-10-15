"""Utilities for creating admin routes.
"""
from __future__ import annotations

import os
from functools import wraps
from typing import Callable, Union

from flask import current_app, redirect, session, url_for
from werkzeug.security import check_password_hash
from werkzeug.wrappers import Response

from .app import bp, db, static_pages

PASSWORD_KEY = "admin_password"

navbar = (
    (
        """
        <img src="https://dsbowen.gitlab.io/hemlock/_static/banner.png" style="max-height:30px;" alt="Hemlock">
        """,
        "https://dsbowen.gitlab.io/hemlock",
    ),
    [
        ("User status", "/admin-status"),
        ("Download", "/admin-download"),
        ("Logout", "/admin-logout"),
    ],
)


def login_required(
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


def password_is_correct() -> bool:
    """Checks if the client has the correct password stored in session.

    Returns:
        bool: Correct password indicator.
    """
    return check_password_hash(
        current_app.config.get("PASSWORD_HASH"),  # type: ignore
        session.get(PASSWORD_KEY, ""),
    )


def in_gitpod_ide() -> bool:
    """Indicates that the admin is developing in the Gitpod IDE.

    Returns:
        bool: Indicator.
    """
    return (
        "GITPOD_HOST" in os.environ
        and os.getenv("VS_CODE_REMOTE", "False").lower() != "true"
    )
