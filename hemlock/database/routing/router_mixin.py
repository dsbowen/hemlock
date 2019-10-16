"""Router mixin

Handles main survey routing. Subclassed by Participant.

Workers integrate with the main survey route as follows:
1. The router mixin executes a routing function.
2. If a subroutine of the routing function requires a worker, the
routing function returns a call to the worker. Otherwise it proceeds as usual.
3. The worker call sends the subroutine to a Redis queue and returns a 
temporary loading page.
4. The loading page connects a socket listening on a dedicated namespace for 
its worker.
5. A worker executes the subroutine when it reaches the head of its Redis 
queue. The subroutine updates the Participant so it can reroute appropriately 
when the job is finished.
6. When the worker finishes executing the subroutine, it emits a 
'job_finished' message on the dedicated namespace.
7. Upon receiving the 'job_finished' message, the socket calls a function to
replace the window location with a new call to the survey route.
"""

from hemlock.app import db
from hemlock.database.private.base import Base

from flask import current_app, flash, redirect, request, url_for


class RouterMixin(Base):
    _route = db.Column(db.String(16), default='_compile')

    def _survey_routing(self):
        """Executed on request to survey route

        If the participant's time has expired, indicate this with an error 
        message and render the current page. Note that we do not want to 
        redirect the participant to a separate time expired page. This is 
        because the last page the participant sees may have important 
        information, such as a completion code.

        Set the route to record response on the POST request after the page 
        was rendered. This indicates that the participant has submitted the 
        page but not yet entered the POST routing sequence. (_record_response 
        is the first routing function of the POST routing sequence.)

        Finally, return the results of the the participant's current routing 
        function.
        """
        page = self.current_page
        if self.time_expired:
            page.error = current_app.time_expired_text
            db.session.commit()
            return self.current_page._render()
        if request.method == 'POST' and self._route == '_render':
            self._route = '_record_response'
        return getattr(self, self._route)()

    def _handle_worker(self, func, worker, next_route=None):
        if worker is None:
            func()
        else:
            if not worker.job_finished:
                return worker()
            worker.reset()
        return None if next_route is None else next_route()