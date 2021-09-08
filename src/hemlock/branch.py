import textwrap

from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable.types import MutablePickleType

from .app import db


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # _user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # _user_head_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    _prev_branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    prev_branch = db.relationship(
        "Branch",
        back_populates="next_branch",
        uselist=False,
        foreign_keys="Branch._prev_branch_id",
    )

    _next_branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))
    next_branch = db.relationship(
        "Branch",
        back_populates="prev_branch",
        uselist=False,
        remote_side=id,
        foreign_keys="Branch._next_branch_id",
    )

    _prev_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    prev_page = db.relationship(
        "Page", back_populates="next_branch", foreign_keys="Branch._prev_page_id"
    )

    pages = db.relationship(
        "Page",
        backref="Branch",
        order_by="Page.index",
        collection_class=ordering_list("index"),
        foreign_keys="Page._branch_id",
    )

    @property
    def start_page(self):
        return self.pages[0] if self.pages else None

    current_page = db.relationship(
        "Page", uselist=False, foreign_keys="Page._branch_head_id"
    )

    navigate = db.Column(MutablePickleType)
    index = db.Column(db.Integer)

    def __init__(self, *pages, navigate=None):
        self.pages = list(pages)
        self.current_page = self.start_page
        self.navigate = navigate

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "

        if not self.pages:
            page_text = ""
        else:
            page_text = "".join([str(page) for page in self.pages])
            page_text = textwrap.indent(page_text, subsequent_indent)

        if not self.next_branch:
            branch_text = ""
        else:
            branch_text = "\n" + textwrap.indent(
                str(self.next_branch), subsequent_indent
            )

        newline = "\n" if page_text and branch_text else ""

        return textwrap.indent(
            f"<{self.__class__.__qualname__} id: {self.id}>\n{page_text}{newline}{branch_text}",
            initial_indent,
        )

    def run_navigate_function(self):
        self.next_branch = self.navigate(self)
        return self

    def go_forward(self):
        if self.current_page is None:
            raise RuntimeError(
                f"You attempted to go forward, but the current page is None on branch \n{self}"
            )

        new_head_index = self.current_page.index + 1
        if new_head_index < len(self.pages):
            self.current_page = self.pages[new_head_index]
        else:
            self.current_page = None

        return self

    def go_back(self):
        if not self.pages or (
            self.current_page is not None and self.current_page is self.start_page
        ):
            raise RuntimeError(
                f"There are no more pages to go back to on branch \n{self}"
            )

        if self.current_page is None:
            self.current_page = self.pages[-1]
        else:
            self.current_page = self.pages[self.current_page.index - 1]

        return self
