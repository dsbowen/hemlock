from __future__ import annotations

import copy
from datetime import datetime

from ..app import db
from .base import Question


# map input types to (HTML format, datetime format)
# where HTML format is the raw format from the post request
# and datetime format is the format expected by python's datetime module
datetime_input_types = {
    "date": ("yyyy-mm-dd", "%Y-%m-%d"),
    "datetime": ("yyyy-mm-ddTHH:MM", "%Y-%m-%dT%H:%M"),
    "datetime-local": ("yyyy-mm-ddTHH:MM", "%Y-%m-%dT%H:%M"),
    "month": ("yyyy-mm", "%Y-%m"),
    "time": ("HH:MM", "%H:%M")
}


class Input(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "input"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/input.html"
    defaults["html_settings"]["input"] = {
        "type": "text",
        "class": ["form-control"]
    }

    @property
    def input_tag(self):
        return self.html_settings["input"]

    def __init__(self, *args, input_tag=None, **kwargs):
        super().__init__(*args, **kwargs)
        if input_tag is not None:
            input_type = input_tag.pop("type", None)
            if input_type is not None:
                self.set_input_type(input_type)

            self.input_tag.update_attrs(input_tag)

    def set_is_valid(self, is_valid: bool=None):
        def add_and_remove_classes(html_attr, remove, add=None):
            classes = self.html_settings[html_attr]["class"]

            if not isinstance(remove, list):
                remove = [remove]
            for class_name in remove:
                try:
                    classes.remove(class_name)
                except ValueError:
                    pass

            if add is not None and add not in classes:
                classes.append(add)

        input_valid_class, input_invalid_class = "is-valid", "is-invalid"
        feedback_valid_class, feedback_invalid_class = "valid-feedback", "invalid-feedback"
        if is_valid is None:
            add_and_remove_classes("input", remove=[input_valid_class, input_invalid_class])
            add_and_remove_classes("feedback", remove=[feedback_valid_class, feedback_invalid_class])
        elif is_valid:
            add_and_remove_classes("input", add=input_valid_class, remove=input_invalid_class)
            add_and_remove_classes("feedback", add=feedback_valid_class, remove=feedback_invalid_class)
        else:
            add_and_remove_classes("input", add=input_invalid_class, remove=input_valid_class)
            add_and_remove_classes("feedback", add=feedback_invalid_class, remove=feedback_valid_class)

        return super().set_is_valid(is_valid)

    def set_input_type(self, input_type="text"):
        # set the placeholder as the input format for browsers that don't support
        # datetime input types
        self.input_tag["type"] = input_type
        if input_type in datetime_input_types and self.input_tag.get("placeholder") is None:
            self.input_tag["placeholder"] = datetime_input_types[input_type][0]
        return self

    def convert_response(self):
        if self.response is None:
            return None
            
        input_type = self.input_tag.get("type", "text")

        if input_type == "number":
            return float(self.response)
        
        if input_type in datetime_input_types:
            _, datetime_format = datetime_input_types[input_type]
            return datetime.strptime(self.response.get_object(), datetime_format)

        return self.response

    def run_validate_functions(self):
        try:
            self.convert_response()
        except ValueError:
            self.set_is_valid(False)
            input_type = self.input_tag.get("type", "text")
            
            if input_type == "number":
                self.feedback = "Please enter a number."
                return False

            if input_type in datetime_input_types:
                html_format, datetime_format = datetime_input_types[input_type]
                self.feedback = f"Please use the format {html_format}. For example, right now it is {datetime.utcnow().strftime(datetime_format)}."
                return False
            
            self.feedback = "Please enter the correct type of response."
            return False

        return super().run_validate_functions()
