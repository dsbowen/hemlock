"""Navbar.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Mapping, Tuple, Union

RawDropdownItem = Union[str, Tuple[str, str], Mapping[str, Union[str, bool]]]
DropdownItem = Dict[str, str]
RawNavitemTuple = Tuple[str, Union[str, Iterable[DropdownItem]]]
RawNavitem = Union[
    str, RawNavitemTuple, Mapping[str, Union[str, bool, RawNavitemTuple]]
]
Navitem = Dict[str, Union[str, List[DropdownItem]]]
RawBrand = Union[str, Tuple[str, str], Mapping[str, str]]
Brand = Dict[str, str]
Navbar = Dict[str, Union[str, Brand, List[Navitem]]]


def convert_brand(brand: RawBrand) -> Brand:
    """Convert navbar brand.

    Args:
        brand (RawBrand): Brand. If a string, this is the brand label. If a tuple, the
            brand will be interpreted as a (label, href) tuple.

    Raises:
        ValueError: Brand must be a string, tuple, or mapping.

    Returns:
        Brand: Converted brand.
    """
    converted = {"label": "", "href": "#", "raw_html": ""}
    if isinstance(brand, str):
        converted["label"] = brand
    elif isinstance(brand, tuple):
        converted.update({"label": brand[0], "href": brand[1]})
    elif isinstance(brand, Mapping):
        converted.update(brand)
    else:
        raise ValueError(f"brand must be a string, tuple, or mapping, got {brand}.")

    return converted


def convert_navitem(item: RawNavitem) -> Navitem:
    """Convert a navitem.

    Args:
        item (RawNavitem): Navitem. If a string, this is the navitem label. If a tuple,
            the navitem will either be interpreted as a (label, href) tuple or a (label,
            dropdown items) tuple.

    Raises:
        ValueError: If a tuple, the second element must be an href (str) or dropdown
            items (iterable).
        ValueError: Navitem must be a string, tuple, or mapping.

    Returns:
        Navitem: Converted navitem.
    """
    converted = {
        "label": "",
        "href": "#",
        "dropdown_items": [],
        "disabled": False,
        "raw_html": "",
    }
    if isinstance(item, str):
        converted["label"] = item
    elif isinstance(item, tuple):
        converted["label"] = item[0]
        if isinstance(item[1], str):
            converted["href"] = item[1]
        elif isinstance(item[1], (list, tuple)):
            converted["dropdown_items"] = [convert_dropdown_item(i) for i in item[1]]
        else:
            raise ValueError(
                f"Second element of item should be a string (href) or a list or tuple of dropdown items, got {item[1]}"
            )
    elif isinstance(item, Mapping):
        converted.update(item)
    else:
        raise ValueError(f"navitem must be a string, tuple, or mapping, got {item}")

    converted["disabled"] = "disabled" if converted["disabled"] else ""
    return converted  # type: ignore


def convert_dropdown_item(item: RawDropdownItem) -> DropdownItem:
    """Convert a dropdown item.

    Args:
        item (RawDropdownItem): Dropdown item. If a string, this is the item label. If a
            tuple, this is interpreted as a (label, href) tuple.

    Raises:
        ValueError: Item must be a string, tuple, or mapping.

    Returns:
        DropdownItem: Converted dropdown item.
    """
    converted = {"label": "", "href": "#", "disabled": False, "raw_html": ""}
    if isinstance(item, str):
        converted["label"] = item
    elif isinstance(item, tuple):
        converted.update({"label": item[0], "href": item[1]})
    elif isinstance(item, Mapping):
        converted.update(item)
    else:
        raise ValueError(f"item must be a string, tuple, or mapping, got {item}.")

    converted["disabled"] = "disabled" if converted["disabled"] else ""
    return converted  # type: ignore
