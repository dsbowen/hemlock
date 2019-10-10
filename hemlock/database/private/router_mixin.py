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

    """Routing"""
    def _survey_route_request(self):
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
    
    def _compile(self):
        """Compile routing function

        This is the initial routing function. It compiles the page's html 
        before rendering.
        """
        page = self.current_page
        if page.compile_worker is not None:
            return page.compile_worker()
        page._compile()
        return self._render()
    
    def _render(self):
        """Render routing function

        If this is the terminal study page, indicate that the participant has completed the study if this has not been done so already.
        """
        page = self.current_page
        if page.terminal and not self.completed:
            self.update_end_time()
            self.completed = True
        db.session.commit()
        return page._render()
    
    def _record_response(self):
        """Record response routing function

        If the participant requested to navigate backward, do so now. 
        Otherwise, if the participant requested to navigate forward, continue 
        to validation.
        """
        self.update_end_time()
        self.completed = False
        self.updated = True
        page = self.current_page
        page._record_response()
        if page.direction_from == 'back':
            return self._navigate()
        return self._validate()

    def _validate(self):
        """Validate routing function"""
        page = self.current_page
        if page.validator_worker is not None:
            return page.validator_worker()
        page._validate()
        return self._submit()

    def _submit(self):
        """Submit routing function
        
        If response was invalid, redirect to the survey route. Otherwise, 
        submit the page.
        """
        page = self.current_page
        if page.direction_from == 'invalid':
            return self._redirect()
        if page.submit_worker is not None:
            return page.submit_worker()
        page._submit()
        return self._navigate()
    
    def _navigate(self):
        """Navigate routing function

        If the requested direction was 'back', go backwards. If the requested direction was 'forward', return the forward routing function.
        """
        page = self.current_page
        if page.direction_from == 'back':
            self._back(page.back_to)
        elif page.direction_from == 'forward':
            self._route = '_forward_routing'
            return self._forward_routing(first_call=True)
        return self._redirect()

    def _forward_routing(self, first_call=False):
        """Forward routing function

        The first time the forward routing function is called for a given 
        survey route request, set the id of the page to which the participant will navigate forward.

        Call the forward navigation function. If this function returns a 
        loading page, render the loading page. Otherwise, return the redirect 
        routing function.
        """
        if first_call:
            page = self.current_page
            self._forward_to_id = (
                None if page.forward_to is None else page.forward_to.id
            )
        loading_page = self.forward()
        if loading_page is not None:
            return loading_page
        self._route = '_redirect'
        return self._redirect()
    
    def _redirect(self):
        """Redirect routing function

        Reset the route to 'compile' and return a GET request to the survey 
        route.
        """
        self._route = 'compile'
        db.session.commit()
        return redirect(url_for('hemlock.survey'))

    """Forward navigation"""
    def _forward(self, forward_to=None):
        """Advance forward to specified Page"""
        if self._forward_to_id is None:
            return self._forward_one()
        while self.current_page.id != self._forward_to_id:
            loading_page = self._forward_one()
            if loading_page is not None:
                return loading_page
    
    def _forward_one(self):
        """Advance forward one page"""
        if (
            self.current_page is not None 
            and self.current_page._eligible_to_insert_branch()
        ):
            loading_page = self._insert_branch(self.current_page)
            if loading_page is not None:
                return loading_page
        else:
            self.current_branch._forward()
        return self._forward_recurse()
    
    def _insert_branch(self, origin):
        """Grow and insert new Branch to branch_stack"""
        if not origin._navigate_finished:
            if origin.navigate_worker is not None:
                return origin.navigate_worker()
            origin.navigate_function()
        origin._navigate_finished = False
        next_branch = origin.next_branch
        self.branch_stack.insert(self.current_branch.index+1, next_branch)
        self._increment_head()
        
    def _forward_recurse(self):
        """Recursive forward function
        
        Advance forward until the next Page is found (i.e. is not None).
        """
        if self.current_page is not None:
            return
        if self.current_branch._eligible_to_insert_branch():
            loading_page = self._insert_branch(self.current_branch)
            if loading_page is not None:
                return loading_page
        else:
            self._decrement_head()
            self.current_branch._forward()
        return self._forward_recurse()
    
    """Backward navigation"""
    def _back(self, back_to=None):
        """Navigate backward to specified Page"""
        if back_to is None:
            return self._back_one()
        while self.current_page.id != back_to.id:
            self._back_one()
            
    def _back_one(self):
        """Navigate backward one Page"""      
        if self.current_page == self.current_branch.start_page:
            self._remove_branch()
        else:
            self.current_branch._back()
        self._back_recurse()
        
    def _remove_branch(self):
        """Remove current branch from the branch stack"""
        self._decrement_head()
        self.branch_stack.pop(self.current_branch.index+1)
        
    def _back_recurse(self):
        """Recursive back function
        
        Navigate backward until previous Page is found.
        """
        if self._found_previous_page():
            return
        if self.current_page is None:
            if self.current_branch.next_branch in self.branch_stack:
                self._increment_head()
            elif not self.current_branch.pages:
                self._remove_branch()
            else:
                self.current_branch._back()
        else:
            self._increment_head()
        self._back_recurse()
    
    def _found_previous_page(self):
        """Indicate that previous page has been found in backward navigation
        
        The previous page has been found when 1) the Page is not None and
        2) it does not branch off to another Branch in the stack.
        """
        return (
            self.current_page is not None 
            and self.current_page.next_branch not in self.branch_stack
            )

    """General navigation and debugging"""
    def _increment_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index+1]
    
    def _decrement_head(self):
        self.current_branch = self.branch_stack[self.current_branch.index-1]
    
    def _view_nav(self):
        """Print branch stack for debugging purposes"""
        self.branch_stack[0].view_nav()