import textwrap

from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable.types import MutablePickleType

from .app import db


class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)

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
        backref="branch",
        order_by="Page.index",
        collection_class=ordering_list("index"),
        foreign_keys="Page._branch_id",
    )

    navigate = db.Column(MutablePickleType)

    def __init__(self, *pages, navigate=None):
        self.pages = list(pages)
        self.navigate = navigate

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "

        if not self.pages:
            page_text = ""
        else:
            page_text = "\n".join([str(page) for page in self.pages])
            page_text = f"\n{textwrap.indent(page_text, subsequent_indent)}"

        return textwrap.indent(
            f"<{self.__class__.__qualname__} id: {self.id}>{page_text}",
            initial_indent,
        )

    def run_navigate_function(self):
        self.next_branch = self.navigate(self)
        return self
