"""Router models

This file defines two router models. 

Each participant has a main Router. The Router has two 'tracks'. When the 
participant requests a new page, the router moves through the 'request' 
track. The request track compiles and renders a new survey page. When the 
participant submits a page, the router moves through the 'submit' track. The 
submit track records the participant's response, validates it, submits it, 
navigates forward, and redirects with a new page request.

The secondary Navigator router is nested in the main Router. It handles 
backward and forward navigation.
"""

from hemlock.app import db
from hemlock.database.private.viewing_page import ViewingPage

from flask import current_app, request, redirect, url_for
from flask_worker import RouterMixin as RouterMixinBase
from flask_worker import set_route


class RouterMixin(RouterMixinBase):
    def run_worker(self, func, worker, next_route, args=[], kwargs={}):
        """Run worker overload"""
        if worker is not None:
            page = super().run_worker(worker, next_route, args, kwargs)
            if worker.job_finished:
                worker.reset()
            return page
        func()
        return next_route(*args, **kwargs)


class Router(RouterMixin, db.Model):
    """Main router
    
    The main router belongs to a Participant. It handles the request and 
    submit tracks.
    """
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    root_name = db.Column(db.String)
    navigator = db.relationship('Navigator', backref='router', uselist=False)

    @property
    def page(self):
        return self.part.current_page

    def __init__(self, root_f):
        self.root_name = root_f.__name__
        self.reset()
        self.navigator = Navigator()

    def reset(self):
        self.current_route = 'compile'
        self.args, self.kwargs = [], {}

    def route(self):
        """Route overload

        If the participant's time has expired, render the current page with 
        a time expired error message.

        By default, the router starts at the beginning of the request track. 
        If the participant has just submitted a page (indicated by a POST 
        request and current route is 'compile'), the router moves to the 
        beginning of the submit track ('record response'). Then route as 
        normal.
        """
        part, page = self.part, self.page
        if part.time_expired:
            page.error = current_app.time_expired_text
            db.session.commit()
            return page._render()
        if request.method == 'POST' and self.current_route == 'compile':
            self.current_route = 'record_response'
        return super().route()

    """Request track"""
    @set_route
    def compile(self):
        return self.run_worker(
            self.page._compile, self.page.compile_worker, self.render
        )
    
    def render(self):
        part, page = self.part, self.page
        if page.terminal and not part.completed:
            part.update_end_time()
            part.completed = True
        page_html = page._render()
        ViewingPage(part, page_html)
        return page_html
    
    """Submit track"""
    def record_response(self):
        part, page = self.part, self.page
        part.update_end_time()
        part.completed = False
        part.updated = True
        page._record_response()
        if page.direction_from == 'back':
            self.navigator.back(page.back_to)
            return self.redirect()
        return self.validate()
    
    @set_route
    def validate(self):
        return self.run_worker(
            self.page._validate, self.page.validate_worker, self.submit
        )
    
    @set_route
    def submit(self):
        page = self.page
        if not page.is_valid():
            return self.redirect()
        return self.run_worker(
            page._submit, page.submit_worker, self.forward_prep, 
        )

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
        """Forward navigation

        Forward navigation uses the Navigator subrouter. If the navigator 
        has not yet started forward navigation (i.e. not nav.in_progress), 
        the main router gets a loading page from nav.forward. Otherwise, it 
        gets a loading page from nav.route.

        The navigator may need a worker to generate a new branch. While the 
        worker's job is in progress, the navigator returns a loading page 
        (which is not None).

        When it finds the next survey page, the navigator return None as the 
        loading page. However, if there is a specified page to which the 
        router is navigating forward (forward_to is not None), it may be 
        necessary to call nav.forward again.
        
        When the navigator has finished, the router redirects the 
        participant to the new survey page.
        """
        nav = self.navigator
        loading_page = (
            nav.forward(forward_to) if not nav.in_progress else nav.route() 
        )
        if loading_page is None and forward_to is not None:
            loading_page = nav.forward(forward_to)
        return loading_page or self.redirect()

    def redirect(self):
        self.reset()
        part = self.part
        url_arg = 'hemlock.{}'.format(self.root_name)
        if part.meta.get('Test') is None:
            return redirect(url_for(url_arg))
        return redirect(url_for(url_arg, part_id=part.id, part_key=part._key))


class Navigator(RouterMixin, db.Model):
    """Navigator subrouter
    
    The navigator subrouter is nexted in the main router. It handles forward 
    and backward navigation.
    """
    id = db.Column(db.Integer, primary_key=True)
    router_id = db.Column(db.Integer, db.ForeignKey('router.id'))
    in_progress = db.Column(db.Boolean)

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
        self.args, self.kwargs = [], {}
        self.in_progress = False

    """Forward navigation"""
    def forward(self, forward_to):
        """Advance forward to specified Page"""
        self.in_progress = True
        if forward_to is None:
            return self.forward_one()
        while self.page != forward_to:
            loading_page = self.forward_one()
            if loading_page is not None:
                return loading_page
    
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
            origin.navigate_function, 
            origin.navigate_worker, 
            self._insert_branch, 
            args=[origin]
        )
    
    def _insert_branch(self, origin):
        branch = origin.next_branch
        self.branch_stack.insert(self.branch.index+1, branch)
        self.increment_head()
        return self.forward_recurse()

    @set_route
    def forward_recurse(self):
        """Recursive forward function
        
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