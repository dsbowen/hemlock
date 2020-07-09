"""Router models

This file defines two router models. 

Each participant has a main Router. The Router has two 'tracks'. When the 
participant requests a new page, the router moves through the 'request' 
track. The request track compiles and renders a new survey page. When the 
participant submits a page, the router moves through the 'submit' track. The 
submit track records the participant's response, validates it, submits it, 
navigates, and redirects with a new page request.

The secondary Navigator router is nested in the main Router. It handles 
backward and forward navigation.
"""

from ...app import db
from .viewing_page import ViewingPage

from flask import current_app, request, redirect, url_for
from flask_worker import RouterMixin as RouterMixinBase
from flask_worker import set_route

from datetime import datetime


class RouterMixin(RouterMixinBase):
    def run_worker(self, func, worker, next_route, *args, **kwargs):
        """
        Run a worker if applicable.

        Parameters
        ----------
        func : callable
            Function to run before navigating to the next route if there is no 
            worker.

        worker : hemlock.WorkerMixin or None
            Worker which executes `func`, if applicable.

        next_route : router method
            The next route to navigate to after executing `func`.

        \*args, \*\*kwargs :
            Arguments and keyword arguments for `next_route`.

        Returns
        -------
        page : str (html)
            Page for the client. This will be a loading page, if the worker is 
            running, or the next page of the survey.        
        """
        if worker is not None:
            if worker.job_finished:
                worker.reset()
                return next_route(*args, **kwargs)
            else:
                return worker()
        func()
        return next_route(*args, **kwargs)


class Router(RouterMixin, db.Model):
    """
    The main router belongs to a Participant. It handles the request and 
    submit tracks.

    Parameters
    ----------
    gen_root : callable
        Callable which generates the root branch.

    Attributes
    ----------
    part : hemlock.Participant
        Participant to whom this router belongs.

    page : hemlock.Page
        The participant's current page.

    view_function : str
        Name of the function which generated the root branch. It is also the 
        name of the view function associated with this router. On redirect, 
        the router, redirects to `url_for(self.view_function)`.

    navigator : hemlock.models.private.Navigator
        A navigator router which handles navigation between pages.
    """
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    view_function = db.Column(db.String)
    navigator = db.relationship('Navigator', backref='router', uselist=False)

    @property
    def page(self):
        return self.part.current_page

    def __init__(self, gen_root):
        self.view_function = gen_root.__name__
        self.navigator = Navigator(gen_root)
        super().__init__(self.compile)

    def __call__(self):
        """Route overload

        If the participant's time has expired, render the current page with 
        a time expired error message.

        The router starts at the beginning of the request track (compile). If 
        the participant has just submitted a page, the router moves to the 
        beginning of the submit track (record response). Then route as normal.

        Returns
        -------
        page : str (html)
            HTML of the participant's next page, or a loading page.
        """
        part, page = self.part, self.page
        if part.time_expired:
            page.error = current_app.time_expired_text
            db.session.commit()
            return page._render()
        if request.method == 'POST' and self.func == self.compile:
            # participant has just submitted the page
            self.func = self.record_response
        return super().__call__()

    """Request track"""
    @set_route
    def compile(self):
        return self.run_worker(
            self.page._compile, self.page.compile_worker, self.render
        )
    
    def render(self):
        part, page = self.part, self.page
        if page.terminal and not part.completed:
            part.end_time = datetime.utcnow()
            part.completed = True
        page_html = page._render()
        part._viewing_pages.append(
            ViewingPage(page_html, first_presentation=not page.viewed)
        )
        page.viewed = True
        return page_html
    
    """Submit track"""
    @set_route
    def record_response(self):
        part, page = self.part, self.page
        part.end_time = datetime.utcnow()
        part.completed = False
        part.updated = True
        page._record_response()
        if page.direction_from == 'back':
            self.navigator.back(page.back_to)
            return self.redirect()
        return self.validate()
    
    @set_route
    def validate(self):
        if not current_app.settings['validate']:
            # validation may be off for testing purposes
            return self.submit()
        return self.run_worker(
            self.page._validate, self.page.validate_worker, self.submit
        )
    
    @set_route
    def submit(self):
        page = self.page
        if not page.is_valid() and current_app.settings['validate']:
            # will redirect to the same page with error messages
            return self.redirect()
        return self.run_worker(
            page._submit, page.submit_worker, self.forward_prep, 
        )

    @set_route
    def forward_prep(self):
        """Prepare for forward navigation
        
        Check if direction_from has been changed by submit functions. If so, 
        navigate appropriately. Otherwise, reset the navigator in preparation 
        for forward navigation.
        """
        page = self.page
        if page.direction_from == 'back':
            self.navigator.back(page.back_to)
        if page.direction_from in ['back', 'invalid']:
            return self.redirect()
        self.navigator.reset()
        return self.forward(page.forward_to)
    
    @set_route
    def forward(self, forward_to):
        """
        Forward navigation uses the Navigator subrouter. If the navigator 
        has not yet started forward navigation (i.e. `not nav.in_progress`), 
        the main router gets a loading page from `nav.forward`. Otherwise, it 
        gets a loading page from `nav.__call__`.

        The navigator may need a worker to generate a new branch. While the 
        worker's job is in progress, the navigator returns a loading page 
        (which is not `None`).

        When it finds the next survey page, the navigator return `None`
        loading page. However, if there is a specified page to which the 
        router is navigating forward (`forward_to is not None`), it may be 
        necessary to call `nav.forward` again.
        
        When the navigator has finished, the router redirects the 
        participant to the new survey page.

        Parameters
        ----------
        forward_to : hemlock.Page
            Page to which to navigate.
        """
        nav = self.navigator
        loading_page = (
            nav.forward(forward_to) if not nav.in_progress else nav() 
        )
        if loading_page is None and forward_to is not None:
            loading_page = nav.forward(forward_to)
        return loading_page or self.redirect()

    @set_route
    def redirect(self):
        self.reset()
        part = self.part
        url_arg = 'hemlock.{}'.format(self.view_function)
        if part.meta.get('Test') is None:
            return redirect(url_for(url_arg))
        # during testing, you may have multiple users running at once
        # in this case, participants much be found be ID, not `current_user`
        return redirect(url_for(url_arg, part_id=part.id, part_key=part._key))


class Navigator(RouterMixin, db.Model):
    """    
    The navigator subrouter is nexted in the main router. It handles forward 
    and backward navigation.

    Attributes
    ----------
    router : hemlock.models.private.Router
        Main router with which the navigator is associated.

    in_progress : bool, default=False
        Indicates that navigation is in progress.
    """
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    in_progress = db.Column(db.Boolean, default=False)

    @property
    def part(self):
        return self.router.part

    @property
    def branch_stack(self):
        return self.part.branch_stack

    @property
    def branch(self):
        return self.part.current_branch

    @branch.setter
    def branch(self, value):
        self.part.current_branch = value

    @property
    def page(self):
        return self.part.current_page

    def reset(self):
        super().reset()
        self.in_progress = False

    """Forward navigation"""
    @set_route
    def forward(self, forward_to=None):
        """Advance forward to specified Page"""
        self.in_progress = True
        if forward_to is None:
            return self.forward_one()
        while self.page != forward_to:
            loading_page = self.forward_one()
            if loading_page is not None:
                return loading_page
    
    @set_route
    def forward_one(self):
        """Advance forward one page"""
        if self.page._eligible_to_insert_branch():
            return self.insert_branch(self.page)
        self.branch._forward()
        return self.forward_recurse()
    
    @set_route
    def insert_branch(self, origin):
        """Grow and insert new branch into the branch stack"""
        return self.run_worker(
            origin._navigate, 
            origin.navigate_worker, 
            self._insert_branch, 
            origin
        )
    
    @set_route
    def _insert_branch(self, origin):
        branch = origin.next_branch
        self.branch_stack.insert(self.branch.index+1, branch)
        self.increment_head()
        return self.forward_recurse()

    @set_route
    def forward_recurse(self):
        """Recursive forward function
    navigator
        Advance forward until the next Page is found (i.e. is not None).
        """
        if self.page is not None:
            return
        if self.branch._eligible_to_insert_branch():
            return self.insert_branch(self.branch)
        self.decrement_head()
        self.branch._forward()
        return self.forward_recurse()
    
    """Back navigation"""
    def back(self, back_to=None):
        """Navigate backward to specified Page"""
        if back_to is None:
            return self.back_one()
        while self.page != back_to:
            self.back_one()
            
    def back_one(self):
        """Navigate backward one Page"""      
        if self.page == self.branch.start_page:
            return self.remove_branch()
        self.branch._back()
        return self.back_recurse()
        
    def remove_branch(self):
        """Remove current branch from the branch stack"""
        self.decrement_head()
        self.branch_stack.pop(self.branch.index+1)
        return self.back_recurse()
        
    def back_recurse(self):
        """Recursive back function
        
        Navigate backward until previous Page is found.
        """
        if self.found_previous_page():
            return
        if self.page is None:
            if self.branch.next_branch in self.branch_stack:
                self.increment_head()
            elif not self.branch.pages:
                return self.remove_branch()
            else:
                self.branch._back()
        else:
            self.increment_head()
        return self.back_recurse()
    
    def found_previous_page(self):
        """Indicate that previous page has been found in backward navigation
        
        The previous page has been found when 1) the Page is not None and
        2) it does not branch off to another Branch in the stack.
        """
        return (
            self.page is not None 
            and self.page.next_branch not in self.branch_stack
        )

    """Move the head of the branch stack"""
    def increment_head(self):
        self.branch = self.branch_stack[self.branch.index+1]
    
    def decrement_head(self):
        self.branch = self.branch_stack[self.branch.index-1]