from typing import Optional
from instaui.components.element import Element
from instaui.components.content import Content
from instaui.vars.types import TMaybeRef


class Button(Element):
    def __init__(
        self,
        label: Optional[TMaybeRef[str]] = None,
        *,
        soft: Optional[TMaybeRef[bool]] = None,
        outline: Optional[TMaybeRef[bool]] = None,
        dash: Optional[TMaybeRef[bool]] = None,
        active: Optional[TMaybeRef[bool]] = None,
        wide: Optional[TMaybeRef[bool]] = None,
    ):
        super().__init__("button")
        self.classes("btn")

        if label is not None:
            with self:
                Content(label)

        if soft is not None:
            self.props({"btn-soft": soft})

        if outline is not None:
            self.props({"btn-outline": outline})

        if dash is not None:
            self.props({"btn-dash": dash})

        if active is not None:
            self.props({"btn-active": active})

        if wide is not None:
            self.props({"btn-wide": wide})
