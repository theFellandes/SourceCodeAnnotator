from dataclasses import dataclass, field
from local_variable_declaration import LocalVariableDeclaration
from formal_parameters import FormalParameters


@dataclass
class MethodDeclaration:
    """
    annotations
    body
    documentation
    modifiers
    name
    parameters
    return_type
    throws
    type_parameters
    """

    documentation = (None,)
    modifiers: dict[str]
    name = (str,)
    return_type = (None,)
    throws = (None,)
    type_parameters = None
    annotations: list[str] = field(default_factory=list)
    body: list[LocalVariableDeclaration] = field(default_factory=list)
    parameters: list[FormalParameters] = field(default_factory=list)
