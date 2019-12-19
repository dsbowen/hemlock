"""Question polymorph imports"""

from hemlock.app import Settings, db
from hemlock.database import Question, HTMLQuestion, ChoiceQuestion, Debug
from hemlock.question_polymorphs.bases import InputGroup

from flask import render_template

from random import choice, random