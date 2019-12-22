
from hemlock.app import db
from hemlock.database.choice import Choice, Option
from hemlock.database.html_question import HTMLQuestion

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates


class ChoiceQuestion(HTMLQuestion):
    @declared_attr
    def default(self):
        return HTMLQuestion.__table__.c.get('default', db.Column(db.Text))

    @validates('choices')
    def validate_choice(self, key, val):
        assert isinstance(val, str) or isinstance(val, Choice)
        if isinstance(val, str):
            if type(self).__name__ in ['Select', 'MultiSelect']:
                return Option(label=val)
            return Choice(label=val)
        return val

    choices = db.relationship(
        'Choice', 
        backref='question',
        order_by='Choice.index',
        collection_class=ordering_list('index'),
        foreign_keys='Choice._question_id'
    )
    
    selected_choices = db.relationship(
        'Choice',
        order_by='Choice._selected_index',
        collection_class=ordering_list('_selected_index'),
        foreign_keys='Choice._selected_id'
    )
    
    nonselected_choices = db.relationship(
        'Choice',
        order_by='Choice._nonselected_index',
        collection_class=ordering_list('_nonselected_index'),
        foreign_keys='Choice._nonselected_id'
    )