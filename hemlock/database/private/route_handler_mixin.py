"""Route handler mixin

Handles main survey routing. Subclassed by Participant
"""

from hemlock.app import db
from hemlock.database.private.base import Base

from flask import current_app, flash, redirect, request, url_for


class RouteHandlerMixin(Base):
    route_status = db.Column(db.String(16))

    def __init__(self, *args, **kwargs):
        self.route_status = 'compile'
        super().__init__(*args, **kwargs)

    def _navigate(self):
        if self.time_expired:
            flash(current_app.time_expired_text)
            return self.current_page.render()
        if self.route_status == 'render' and request.method == 'POST':
            self.route_status = 'record_response'
        return getattr(self, self.route_status)()
    
    def compile(self):
        page = self.current_page
        if page.compile_worker is not None:
            return page.compile_worker()
        page.compile()
        return self.render()
    
    def render(self):
        page = self.current_page
        if page.terminal and not self.completed:
            self.update_end_time()
            self.completed = True
        db.session.commit()
        return page.render()
    
    def record_response(self):
        page = self.current_page
        self.update_end_time()
        self.completed = False
        self.updated = True
        page.record_response()
        if page.direction_from == 'back':
            return self.navigate()
        return self.validate()

    def validate(self):
        page = self.current_page
        if page.validator_worker is not None:
            return page.validator_worker()
        page.validate()
        return self.submit()

    def submit(self):
        page = self.current_page
        if page.submit_worker is not None:
            return page.submit_worker()
        page.submit()
        return self.navigate()
    
    def navigate(self):
        page = self.current_page
        if page.direction_from == 'back':
            self.back(page.back_to)
        elif page.direction_from == 'forward':
            self.route_status = 'forward_routing'
            return self.forward_routing(first_call=True)
        return self.redirect()

    def forward_routing(self, first_call=False):
        if first_call:
            page = self.current_page
            self._forward_to_id = (
                None if page.forward_to is None else page.forward_to.id
            )
        loading_page = self.forward()
        if loading_page is None:
            self.route_status = 'redirect'
            return self.redirect()
        return loading_page
    
    def redirect(self):
        self.route_status = 'compile'
        db.session.commit()
        return redirect(url_for('hemlock.survey'))