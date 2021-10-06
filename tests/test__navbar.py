import pytest

from hemlock import Page, create_test_app
from hemlock._navbar import convert_brand, convert_navitem, convert_dropdown_item


class TestConvertBrand:
    def test_from_str(self):
        label = "label"
        assert convert_brand(label) == {"label": label, "href": "#", "raw_html": ""}

    def test_from_tuple(self):
        assert convert_brand(("label", "href")) == {
            "label": "label",
            "href": "href",
            "raw_html": "",
        }

    def test_from_mapping(self):
        assert convert_brand({"raw_html": "raw_html"}) == {
            "label": "",
            "href": "#",
            "raw_html": "raw_html",
        }


class TestConvertNavitem:
    def test_from_str(self):
        label = "label"
        assert convert_navitem(label) == {
            "label": label,
            "href": "#",
            "dropdown_items": [],
            "disabled": "",
            "raw_html": "",
        }

    def test_from_tuple(self):
        assert convert_navitem(("label", "href")) == {
            "label": "label",
            "href": "href",
            "dropdown_items": [],
            "disabled": "",
            "raw_html": "",
        }

    def test_dropdown(self):
        assert convert_navitem(("label", ["dropdown"])) == {
            "label": "label",
            "href": "#",
            "dropdown_items": [convert_dropdown_item("dropdown")],
            "disabled": "",
            "raw_html": "",
        }

    def test_from_mapping(self):
        item = convert_navitem({"disabled": True, "raw_html": "raw_html"})
        assert item["disabled"] == "disabled"
        assert item["raw_html"] == "raw_html"


class TestConvertDropdownItem:
    def test_from_str(self):
        label = "label"
        assert convert_dropdown_item(label) == {
            "label": label,
            "href": "#",
            "disabled": "",
            "raw_html": "",
        }

    def test_from_tuple(self):
        assert convert_dropdown_item(("label", "href")) == {
            "label": "label",
            "href": "href",
            "disabled": "",
            "raw_html": "",
        }

    def test_from_mapping(self):
        item = convert_dropdown_item({"disabled": True, "raw_html": "raw_html"})
        assert item["disabled"] == "disabled"
        assert item["raw_html"] == "raw_html"


def test_in_page():
    app = create_test_app()
    with app.test_request_context():
        Page(
            navbar=(
                ("Brand", "https://my-brand-href.html"),
                [
                    "Link 0",
                    ("Link 1", "https://link1.html"),
                    {"label": "Link 2", "disabled": True},
                    (
                        "Dropdown",
                        [
                            "Dropdown link 0",
                            ("Dropdown link 1", "https://dropdown-link1.html"),
                            {"label": "Dropdown link 2", "disabled": True}
                        ]
                    )
                ]
            )
        ).render()
