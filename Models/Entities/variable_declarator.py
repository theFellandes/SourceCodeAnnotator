from dataclasses import dataclass, field
from class_creator import ClassCreator
from literal import Literal


@dataclass
class VariableDeclarator:
    """
    annotations
    body
    documentation
    extends
    implements
    modifiers
    name
    type_parameters
    """

    dimensions: list[str] = field(default_factory=list)
    initializer: ClassCreator | Literal = ClassCreator() | Literal()
    name: str = ""
