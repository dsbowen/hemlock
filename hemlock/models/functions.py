"""# Function models"""

from ..app import db
from .bases import Base
from .branch import Branch
from .page import Page
from .question import Question

from sqlalchemy_function import FunctionMixin

from random import random

def _set_parent(model, parent):
    if isinstance(parent, Branch):
        model.branch = parent
    elif isinstance(parent, Page):
        model.page = parent
    elif isinstance(parent, Question):
        model.question = parent


class FunctionRegistrar(FunctionMixin, Base):
    """
    Mixin for Function models which provides a method for function registration. 
    
    Inherits from `sqlalchemy_function.FunctionMixin`. See 
    <https://dsbowen.github.io/sqlalchemy-function/>.
    """
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def register(self, func):
        """
        This decorator registers a function.

        Parameters
        ----------
        func : callable
            The function to register.
        """
        def add_function(parent, *args, **kwargs):
            cls(parent, func, *args, **kwargs)
        setattr(cls, func.__name__, add_function)
        return func


class Compile(Function, db.Model):
    """
    Helps compile a page or question html before it is rendered and displayed to a participant.

    Inherits from `hemlock.FunctionRegistrar`.

    Parameters
    ----------
    parent : hemlock.Page, hemlock.Question, or None, default=None
        The page or question to which this function belongs.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `parent` parameter.

    question : hemlock.Question or None
        Set from the `parent` parameter.
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __init__(self, page=None, *args, **kwargs):
        _set_parent(self, parent)
        super().__init__(*args, **kwargs)


class Validate(Function, db.Model):
    """
    Validates a participant's response.

    Inherits from `hemlock.FunctionRegistrar`.

    Parameters
    ----------
    parent : hemlock.Page, hemlock.Question, or None, default=None
        The page or question to which this function belongs.

    Attributes
    ----------
    error_msg : str or None
        If the validate function returns an error message, the `error_msg`
        attribute is returned instead of the output of the validate function.
        You can set this by passing in an `error_msg` keyword argument to the
        constructor.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `parent` parameter.

    question : hemlock.Question or None
        Set from the `parent` parameter.
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    error_msg = db.Column(db.Text)

    def __init__(self, parent=None, *args, **kwargs):
        _set_parent(self, parent)
        self.error_msg = kwargs.pop('error_msg', None)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Returns
        -------
        error_msg : str or None
            Return `None` if there is no error. If there is an error, return
            `self.error_msg` or the output of `self.func`.
        """
        error_msg = super().__call__(*args, **kwargs)
        if error_msg:
            return self.error_msg or error_msg


class Submit(Function, db.Model):
    """
    Runs after a participant has successfully submitted a page.

    Inherits from `hemlock.FunctionRegistrar`.

    Parameters
    ----------
    parent : hemlock.Page, hemlock.Question, or None, default=None
        The page or question to which this function belongs.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `parent` parameter.

    question : hemlock.Question or None
        Set from the `parent` parameter.
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    def __init__(self, parent=None, *args, **kwargs):
        _set_parent(self, parent)
        super().__init__(*args, **kwargs)


class Debug(Function, db.Model):
    """
    Run to help debug the survey.

    Inherits from `hemlock.FunctionRegistrar`.

    Parameters
    ----------
    parent : hemlock.Page, hemlock.Question, or None, default=None
        The page or question to which this function belongs.

    Attributes
    ----------
    p_exec : float, default=1.
        Probability that the debug function will execute. You can set this by
        passing in an `p_exec` keyword argument to the constructor.

    Relationships
    -------------
    page : hemlock.Page or None
        Set from the `parent` parameter.

    question : hemlock.Question or None
        Set from the `parent` parameter.
    """
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    p_exec = db.Column(db.Float)

    def __init__(self, parent=None, *args, **kwargs):
        _set_parent(self, parent)
        self.p_exec = kwargs.pop('p_exec', 1.)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Execute the debug function with probability `self.p_exec`.
        """
        if random() < self.p_exec:
            return super().__call__(*args, **kwargs)


class Navigate(Function, db.Model):
    """
    Creates a new branch to which the participant will navigate.

    Parameters
    ----------
    parent : hemlock.Branch, hemlock.Page, or None, default=None
        The branch or page to which this function belongs.

    Relationships
    -------------
    branch : hemlock.Branch
        Set from the `parent` parameter.

    page : hemlock.Page
        Set from the `parent` parameter.
    """
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    def __init__(self, parent=None, *args, **kwargs):
        _set_parent(parent)
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Create a new branch and 'link' it to the tree. Linking in the new branch involves setting the `next_branch` and `origin_branch` or `origin_page` relationships.
        """
        next_branch = super().__call__(*args, **kwargs)
        assert isinstance(next_branch, Branch)
        parent = self.branch or self.page
        if parent is not None:
            self._set_relationships(parent, next_branch)
        next_branch.current_page = next_branch.start_page
        return next_branch

    def _set_relationships(self, parent, next_branch):
        """Set relationships between next_branch and its origin"""
        parent.next_branch = next_branch
        if isinstance(parent, Branch):
            next_branch.origin_page = None
            next_branch.origin_branch = parent
        else:
            next_branch.origin_branch = None
            next_branch.origin_page = parent