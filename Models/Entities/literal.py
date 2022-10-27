from dataclasses import dataclass, field


@dataclass
class Literal:
    """
    postfix_operators: list[str]
    prefix_operators: list[str]
    qualifier
    selectors: list[str]
    value: int
    """
    postfix_operators: list[str] = field(default_factory=list),
    prefix_operators: list[str] = field(default_factory=list),
    qualifier = None,
    selectors: list[str] = field(default_factory=list),
    value: int = 0
