from dataclasses import dataclass, field


@dataclass
class JavaAST:
    imports: list[str] = field(default_factory=list)
