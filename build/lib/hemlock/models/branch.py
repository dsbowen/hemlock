"""# Branch"""

from ..app import db
from .bases import BranchingBase

from sqlalchemy.ext.orderinglist import ordering_list


class Branch(BranchingBase, db.Model):
    """
    Branches are stacked in a participant's branch stack. A branch contains a 
    queue of pages which it displays to its participant.

    Inherits from [`hemlock.models.Base`](bases.md).

    Parameters
    ----------
    \*pages : hemlock.Page
        Pages which belong to this branch.

    Attributes
    ----------
    index : int or None, default=None
        Order in which this branch appears in its participant's branch stack.

    Relationships
    -------------
    part : hemlock.Participant
        Participant to whose branch stack this page belongs.

    origin_branch : hemlock.Branch
        The branch from which this branch originated.

    next_branch : hemlock.Branch
        The branch which originated from this branch.

    origin_page : hemlock.Page
        The page from which this branch originated. Note that branches can originate from other branches or pages.

    pages : list of hemlock.Page
        The queue of pages belonging to this branch.

    start_page : hemlock.Page or None
        The first page in the page queue, if non-empty.

    current_page : hemlock.Page
        Current page of this branch (head of the page queue).

    embedded : list of hemlock.Embedded
        Embedded data elements.

    data_elements : list of hemlock.DataElement
        All data elements belonging to this branch, in order of embedded data 
        then page data.

    navigate_function : hemlock.Navigate
        Navigate function which returns a new branch once the participant has 
        reached the end of this branch (i.e. the end of the page queue 
        associated with this branch).

    navigate_worker : hemlock.NavigateWorker
        Worker which handles complex navigate functions.

    Examples
    --------
    ```python
    from hemlock import Branch, Label, Page, push_app_context

    app = push_app_context()

    Branch(
    \    Page(Label('<p>Hello World</p>')),
    \    Page(Label('<p>Hello Moon</p>')),
    \    Page(Label('<p>Hello Star</p>'))
    ).preview()
    ```

    This will open all of the branch's pages in separate tabs.
    """
    id = db.Column(db.Integer, primary_key=True)
    
    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _part_head_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    
    _origin_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    origin_branch = db.relationship(
        'Branch',
        back_populates='next_branch',
        uselist=False,
        foreign_keys='Branch._origin_branch_id'
    )
        
    _next_branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    next_branch = db.relationship(
        'Branch',
        back_populates='origin_branch',
        uselist=False,
        remote_side=id,
        foreign_keys='Branch._next_branch_id'
    )
    
    _origin_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    origin_page = db.relationship(
        'Page', 
        back_populates='next_branch',
        foreign_keys='Branch._origin_page_id'
    )
    
    pages = db.relationship(
        'Page', 
        backref='branch', 
        order_by='Page.index',
        collection_class=ordering_list('index'),
        foreign_keys='Page._branch_id'
    )
    
    @property
    def start_page(self):
        """Return the start of the page queue"""
        return self.pages[0] if self.pages else None
        
    current_page = db.relationship(
        'Page', 
        uselist=False,
        foreign_keys='Page._branch_head_id'
    )
        
    embedded = db.relationship(
        'Embedded', 
        backref='branch',
        order_by='Embedded.index',
        collection_class=ordering_list('index')
    )
        
    @property
    def data_elements(self):
        elements = []
        elements += self.embedded
        [elements.extend(p.data_elements) for p in self.pages]
        return elements
        
    navigate_function = db.relationship(
        'Navigate',
        backref='branch', 
        uselist=False
    )
    navigate_worker = db.relationship(
        'NavigateWorker',
        backref='branch', 
        uselist=False
    )

    index = db.Column(db.Integer)

    def __init__(self, *pages, **kwargs):
        self.pages = list(pages)
        super().__init__(**kwargs)

    def preview(self, driver=None):
        """
        Preview the page queue in the a browser window.

        Parameters
        ----------
        driver : selenium.webdriver.chrome.webdriver.WebDriver or None, default=None
            Driver to preview page debugging. If `None`, the page will be
            opened in a web browser.

        Returns
        -------
        self : helock.Branch
        """
        [p.preview(driver) for p in self.pages]
        self

    def view_nav(self):
        """
        Print this branch's page queue for debugging purposes.
        
        Returns
        -------
        self : hemlock.Branch
        """
        # Note to self: the commented lines were very useful for me when 
        # debugging the navigation system; less so for users

        # HEAD_PART = '<== head branch of participant'
        # HEAD_BRANCH = '<== head page of branch'
        indent = 4*(0 if self.index is None else self.index)
        # head_part = HEAD_PART if self == self.part.current_branch else ''
        # print(' '*indent, self, head_part)
        print(' '*indent, self)
        [p.view_nav(indent) for p in self.pages]
        # head_branch = HEAD_BRANCH if None == self.current_page else ''
        # print(' '*indent, None, head_branch)
        if self.next_branch in self.part.branch_stack:
            self.next_branch.view_nav()
        return self
        
    def _forward(self):
        """Advance forward to the next page in the queue"""
        if self.current_page is not None:
            new_head_index = self.current_page.index + 1
            if new_head_index == len(self.pages):
                self.current_page = None
            else:
                self.current_page = self.pages[new_head_index]
        return self
    
    def _back(self):
        """Return to previous page in queue"""
        if self.pages:
            if self.current_page is None:
                self.current_page = self.pages[-1]
            else:
                new_head_index = self.current_page.index - 1
                self.current_page = self.pages[new_head_index]
        return self