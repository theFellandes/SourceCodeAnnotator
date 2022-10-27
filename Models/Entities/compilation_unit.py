from dataclasses import dataclass, field
from class_declaration import ClassDeclaration


@dataclass
class CompilationUnit:
    package: None
    imports: list[str] = field(default_factory=list)
    types: list[ClassDeclaration] = field(default_factory=list)
