"""Login"""

from ...app import bp, db
from ...models import Page
from ...qpolymorphs import Input
from .utils import LOGIN_REQUIRED, render, researcher_page, session_store

from flask import current_app, redirect, request, session, url_for
from werkzeug.security import check_password_hash

from functools import wraps

PASSWORD_INCORRECT = 'Incorrect password.'
PASSWORD_PROMPT = '<p>Please enter your password.</p>'

@bp.route('/login', methods=['GET','POST'])
def login():
    """Login view function"""
    login_p = login_page()
    if request.method == 'POST':
        password = login_p._record_response().questions[0].response or ''
        session_store('password', password)
        if login_p._validate():
            return login_successful()
    return render(login_p)

@researcher_page('login')
def login_page():
    """Create login page"""
    login_p = Page(
        Input(PASSWORD_PROMPT, input_type='password'), 
        back=False, 
        forward='Login'
    )
    login_p.body.select_one('#forward-btn')['class'] += ' w-100'
    login_p.validate_functions = check_password
    return login_p

def check_password(login_page):
    """Check the input password against researcher password"""
    if not password_correct():
        return PASSWORD_INCORRECT

def password_correct():
    """Indicate that the session password is correct"""
    if not current_app.settings['password']:
        return True
    if 'password' not in session:
        return False
    return check_password_hash(
        current_app.settings['password_hash'], session['password']
    )

def login_successful():
    """Process successful login

    Clear login page and redirect to requested page.
    """
    login_page().clear_error().clear_response()
    db.session.commit()
    requested = request.args.get('requested') or 'status'
    return redirect(url_for('hemlock.{}'.format(requested)))

def researcher_login_required(func):
    """Decorator requiring researcher login"""
    @wraps(func)
    def login_requirement():
        if not password_correct():
            login_page().error = LOGIN_REQUIRED
            db.session.commit()
            return redirect(url_for('hemlock.login', requested=func.__name__))
        return func()
    return login_requirement

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hemlock.login'))