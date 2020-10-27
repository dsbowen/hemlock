"""Login"""

from ...app import bp, db
from ...models import Page
from ...qpolymorphs import Input

from flask import current_app, redirect, request, session, url_for
from werkzeug.security import check_password_hash

from functools import wraps

@bp.route('/login', methods=['GET','POST'])
def login():
    """Login view function"""
    def login_page():
        error = None
        if request.args.get('incorrect_password'):
            error = 'The password you entered was incorrect.'
        elif request.args.get('requested'):
            error = 'Login required to access this page.'
        return Page(
            Input(
                'Please enter your password.', 
                type='password', key='password'
            ),
            error=error, forward='Login'
        )._render()

    if request.method == 'GET':
        return login_page()
    # request method is POST
    requested = request.args.get('requested', 'status')
    session['password'] = request.form.get('password')
    if password_is_correct():
        return redirect(url_for('hemlock.{}'.format(requested)))
    return redirect(
        url_for('hemlock.login', requested=requested, incorrect_password=True)
    )

def password_is_correct():
    """Indicate that the session password is correct"""
    if not current_app.config.get('PASSWORD'):
        return not session.get('password')
    if 'password' not in session:
        return False
    return check_password_hash(
        current_app.config.get('PASSWORD_HASH'), session['password']
    )

def researcher_login_required(func):
    """Decorator requiring researcher login"""
    @wraps(func)
    def login_required():
        if password_is_correct():
            return func()
        return redirect(url_for('hemlock.login', requested=func.__name__))

    return login_required

@bp.route('/logout')
def logout():
    if 'download-page-id' in session:
        page = Page.query.get(session['download-page-id'])
        if page:
            db.session.delete(page)
            db.session.commit()
    session.clear()
    return redirect(url_for('hemlock.login'))