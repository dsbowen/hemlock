from hemlock.app import db

from flask import current_app
from flask_worker import RouterMixin as RouterMixinBase
from flask_worker import set_route


class RouterMixin(RouterMixinBase):
    def run_worker(self, func, worker, next_route, args=[], kwargs={}):
        if worker is not None:
            return super().run_worker(worker, next_route, args, kwargs)
        func()
        return next_route(*args, **kwargs)


class Router(RouterMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    navigator = db.relationship(
        'Navigator',
        backref='router',
        uselist=False
    )

    @property
    def page(self):
        return self.part.current_page

    def __init__(self):
        self.current_route = 'compile'
        self.navigator = Navigator()

    def route(self):
        part, page = self.part, self.page
        if part.time_expired:
            page.error = current_app.time_expired_text
            db.session.commit()
            return page._render()
        if request.method == 'POST' and self.current_route == 'compile':
            self.current_route = 'record_response'
        return super().route()

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
        return page._render()
    
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
        if page.direction_from == 'invalid':
            return self.redirect()
        self.navigator.reset()
        return self.run_worker(
            page._submit, page.submit_worker, self.forward, 
            args=[page.forward_to]
        )
    
    @set_route
    def forward(self, forward_to):
        nav = self.navigator
        if not nav.in_progress:
            loading_page = nav.forward(forward_to)
        else:
            loading_page = nav.route()
        if nav.in_progress:
            loading_page = loading_page or nav.forward(forward_to)
        return loading_page or self.redirect()

    def redirect(self):
        self.current_route = 'compile'
        return redirect(url_for('hemlock.survey'))


class Navigator(RouterMixin, db.Model):
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

    @property
    def page(self):
        return self.part.current_page

    def reset(self):
        self.args, self.kwargs = [], {}
        self.in_progress = False

    """Forward navigation"""
    def forward(self, forward_to):
        if forward_to is None:
            loading_page = None if self.in_progress else self.forward_one()
        else:
            while self.page != forward_to:
                loading_page = self.forward_one()
                if loading_page is not None:
                    break
        self.in_progress = loading_page is not None
        return loading_page
    
    def forward_one(self):
        if self.page._eligible_to_insert_branch():
            return self.insert_branch(self.page)
        self.branch._forward()
        return self.forward_recurse()
    
    @set_route
    def insert_branch(self, origin):
        return self.run_worker(
            origin.navigate, origin.navigate_worker, self._insert_branch,
            args=[origin]
        )
    
    def _insert_branch(self, origin):
        branch = origin.next_branch
        self.branch_stack.insert(self.branch.index+1, branch)
        self.increment_head()
        return self.forward_recurse()

    @set_route
    def forward_recurse(self):
        if self.page is not None:
            return
        if self.branch._eligible_to_insert_branch():
            return self.insert_branch(branch)
        self.decrement_head()
        self.branch._forward()
        return self.forward_recurse()
    
    """Back navigation"""
    def back(self, back_to=None):
        """Navigate backward to specified Page"""
        if back_to is None:
            return self._back_one()
        while self.current_page != back_to:
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
        self.part.current_branch = self.branch_stack[self.branch.index+1]
    
    def decrement_head(self):
        self.part.current_branch = self.branch_stack[self.branch.index-1]