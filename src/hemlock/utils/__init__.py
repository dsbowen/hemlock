"""Utilities.
"""
from __future__ import annotations

import os
import subprocess
from typing import Any

import flask
from flask import request
from werkzeug.wrappers.response import Response


def redirect(location: str, *args: Any, **kwargs: Any) -> Response:
    """Custom redirect for compatibility with Gitpod.

    Replace `flask.redirect` with this function.

    Args:
        location (str): Original redirect URL.
        *args (Any): Passed to `flask.redirect`.
        **kwargs (Any): Passed to `flask.redirect`.

    Returns:
        Response: Redirect response.
    """
    if (
        location.startswith("/")
        and "GITPOD_HOST" in os.environ
        and os.environ.get("VS_CODE_REMOTE", "False").lower() != "true"
    ):  # pragma: no cover
        # change URL root to gitpod workspace url
        url_root = request.url_root
        if "http" in url_root:
            url_root = url_root.lstrip("http://")

        index = url_root.index(":") + 1
        port = url_root[index : index + 4]  # port is the 4 numbers after ":"
        gp_url_port = subprocess.check_output(f"gp url {port}", shell=True)
        location = gp_url_port.decode("utf-8").strip() + location

    return flask.redirect(location, *args, **kwargs)
