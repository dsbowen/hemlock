"""Routing functions"""

def set_route(func):
    """Set the route as the routing function name"""
    def with_route_setting(part):
        part._route = func.__name__
        return func()
    return with_route_setting


@set_route
class RoutingFunctionsMixin():
    _forward_route = db.Column(db.String(16), default='_forward')
    _forward_to_id = db.Column(db.Integer)

    def _compile(self):
        """Compile routing function

        This is the initial routing function. It compiles the page's html 
        before rendering.
        """
        page = self.current_page
        return self._handle_worker(
            page._compile, page.compile_worker, self._render
        )
    
    def _render(self):
        """Render routing function

        If this is the terminal study page, indicate that the participant has 
        completed the study if this has not been done so already.
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
        return self._handle_worker(
            page._validate, page.validate_worker, self._submit
        )

    def _submit(self):
        """Submit routing function
        
        If response was invalid, redirect to the survey route. Otherwise, 
        submit the page.
        """
        page = self.current_page
        if page.direction_from == 'invalid':
            return self._redirect()
        return self._handle_worker(
            page._submit, page.submit_worker, self._navigate
        )
    
    def _navigate(self):
        """Navigate routing function

        If the requested direction was 'back', go backwards. If the requested direction was 'forward', return the forward routing function.
        """
        page = self.current_page
        if page.direction_from == 'back':
            self._back(page.back_to)
        elif page.direction_from == 'forward':
            self._route = '_forward_routing'
            self._forward_route = '_forward'
            self._forward_to_id = page.forward_to.id
            return self._forward_routing()
        return self._redirect()

    def _forward_routing(self):
        """Forward routing function

        The first time the forward routing function is called for a given 
        survey route request, set the id of the page to which the participant will navigate forward.

        Call the forward navigation function. If this function returns a 
        loading page, render the loading page. Otherwise, return the redirect 
        routing function.
        """
        loading_page = getattr(self, self._forward_route)()
        if loading_page is not None:
            return loading_page
        return self._redirect()
    
    def _redirect(self):
        """Redirect routing function

        Reset the route to 'compile' and return a GET request to the survey 
        route.
        """
        self._route = 'compile'
        db.session.commit()
        return redirect(url_for('hemlock.survey'))