from flask import redirect, request
from flask_login import current_user, login_user, logout_user

from .app import bp, db
from .user import User


@bp.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.get_tree().page.is_first_page:
            return redirect(User.default_url_rule)

    # TODO: handle restart and screenout pages

    if current_user.is_authenticated:
        logout_user()

    meta_data = dict(request.args)
    meta_data["ipv4"] = request.remote_addr
    user = User(meta_data=meta_data)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(User.default_url_rule)
