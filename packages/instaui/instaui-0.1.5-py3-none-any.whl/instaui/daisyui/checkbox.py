from typing import Optional
from instaui.components.element import Element
from instaui.vars.types import TMaybeRef
from instaui.vars.web_computed import WebComputed


class Checkbox(Element):
    def __init__(self, checked: TMaybeRef[bool] = False):
        super().__init__("input")
        self.classes("checkbox")
        self.props({"type": "checkbox"})

        if checked is not None:
            if isinstance(checked, WebComputed):
                self.props({"value": checked})
            else:
                self.vmodel(checked, prop_name="value", is_html_component=True)
