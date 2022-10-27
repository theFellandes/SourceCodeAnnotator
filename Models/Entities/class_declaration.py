from dataclasses import dataclass, field


@dataclass
class ClassDeclaration:
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
    body: list[str] = field(default_factory=list)
    documentation = None,
    extends = None,
    implements = None,
    modifiers: set = field(default_factory=set),
    name = str,
    type_parameters = None
