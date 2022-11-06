from dataclasses import dataclass, field


@dataclass
class ReferenceType:
    """
    arguments
    dimensions: list
    name: str
    sub_type
    """

    arguments = (None,)
    dimensions: list = (field(default_factory=list),)
    name: str = ("",)
    sub_type = None
