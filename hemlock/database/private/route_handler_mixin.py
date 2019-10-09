"""Route handler mixin

Handles main survey routing. Subclassed by Participant

Workers integrate with the main survey route as follows:
1. Based on the request method, the survey view function returns a get() or 
post() function.
2. If a subroutine of the get() or post() function requires a worker, the
function sends the subroutine to a Redis queue and renders a temporary loading
page.
3. The loading page connects a socket listening on a dedicated namespace for 
the page which called the worker.
4. A worker grabs the subroutine from the Redis queue and executes it. When
finished, the page to which the subroutine belongs stores an indicator that
the job has finished.
5. When the worker finishes executing the subroutine, it emits a 
'job_finished' message on the dedicated namespace.
6. Upon receiving the 'job_finished' message, the socket calls a function to
replace the window location with a new call to the survey route. Because the
page now indicates that the subroutine has finished, it knows not to execute
the subroutine again on the new request.
"""

from hemlock.app import db
from hemlock.database.private.base import Base

from flask import current_app, flash, redirect, request, url_for


class RouteHandlerMixin(Base):
    route_status = db.Column(db.String(16))

    def __init__(self, *args, **kwargs):
        self.route_status = 'compile'
        super().__init__(*args, **kwargs)

    def _survey_route(self):
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