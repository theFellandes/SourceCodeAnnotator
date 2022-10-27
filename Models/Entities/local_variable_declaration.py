from dataclasses import dataclass, field
from variable_declarator import VariableDeclarator
from reference_type import ReferenceType


@dataclass
class LocalVariableDeclaration:
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
    annotations: list[str] = field(default_factory=list)
    declarators: list[VariableDeclarator] = field(default_factory=list)
    modifiers: set = field(default_factory=set),
    type: ReferenceType = ReferenceType()
