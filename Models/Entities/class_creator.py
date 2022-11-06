from dataclasses import dataclass, field
from reference_type import ReferenceType


@dataclass
class ClassCreator:
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

    arguments = list[str] = (field(default_factory=list),)
    body = (None,)
    constructor_type_arguments = (None,)
    postfix_operators: list[str] = (field(default_factory=list),)
    prefix_operators: list[str] = (field(default_factory=list),)
    qualifier = (None,)
    selectors: list[str] = (field(default_factory=list),)
    type: ReferenceType = ReferenceType()
