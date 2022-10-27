from compilation_unit import CompilationUnit
from class_declaration import ClassDeclaration
from method_declaration import MethodDeclaration
from local_variable_declaration import LocalVariableDeclaration
from variable_declarator import VariableDeclarator
from reference_type import ReferenceType
from basic_type import BasicType
from statement_expression import StatementExpression
from assignment import Assignment
from formal_parameter import FormalParameter
from class_creator import ClassCreator
from literal import Literal
from member_reference import MemberReference
from method_invocation import MethodInvocation


CompilationUnit(
        imports=[],
        package=None,
        types=[
            ClassDeclaration(
                annotations=[],
                body=[
                    MethodDeclaration(
                        annotations=[],
                        body=[
                            LocalVariableDeclaration(
                                annotations=[],
                                declarators=[
                                    VariableDeclarator(
                                        dimensions=[],
                                        initializer=ClassCreator(
                                            arguments=[],
                                            body=None,
                                            constructor_type_arguments=None,
                                            postfix_operators=[],
                                            prefix_operators=[],
                                            qualifier=None,
                                            selectors=[],
                                            type=ReferenceType(
                                                arguments=None,
                                                dimensions=None,
                                                name='hashmap',
                                                sub_type=None
                                            )
                                        ),
                                        name='map'
                                    )
                                ],
                                modifiers=set(),
                                type=ReferenceType(
                                    arguments=None,
                                    dimensions=[],
                                    name='hashmap',
                                    sub_type=None
                                )
                            ),
                            LocalVariableDeclaration(
                                annotations=[],
                                declarators=[
                                    VariableDeclarator(
                                        dimensions=[],
                                        initializer=Literal(
                                            postfix_operators=[],
                                            prefix_operators=[],
                                            qualifier=None,
                                            selectors=[],
                                            value=0
                                        ),
                                        name='testing'
                                    )
                                ],
                                modifiers=set(),
                                type=ReferenceType(
                                    arguments=None,
                                    dimensions=[],
                                    name='var',
                                    sub_type=None
                                )
                            ),
                            LocalVariableDeclaration(
                                annotations=[],
                                declarators=[
                                    VariableDeclarator(
                                        dimensions=[],
                                        initializer=Literal(
                                            postfix_operators=[],
                                            prefix_operators=[],
                                            qualifier=None,
                                            selectors=[],
                                            value=0
                                        ),
                                        name='testing2'
                                    )
                                ],
                                modifiers=set(),
                                type=BasicType(
                                    dimensions=[],
                                    name=int
                                )
                            ),
                            StatementExpression(
                                expression=Assignment(
                                    expressionl=MemberReference(
                                        member='testing',
                                        postfix_operators=[],
                                        prefix_operators=[],
                                        qualifier=,
                                        selectors=[]
                                    ),
                                    type ==,
                                    value=MemberReference(
                                        member='testing2',
                                        postfix_operators=[],
                                        prefix_operators=[],
                                        qualifier=,
                                        selectors=[]
                                    )
                                ),
                                label=None
                            ),
                            StatementExpression(
                                expression=MethodInvocation(
                                    arguments=[
                                        Literal(
                                            postfix_operators=[],
                                            prefix_operators=[],
                                            qualifier=None,
                                            selectors=[],
                                            value="Hello World!"
                                        )
                                    ],
                                    member=println,
                                    postfix_operators=[],
                                    prefix_operators=[],
                                    qualifier=System.out,
                                    selectors=[],
                                    type_arguments=None
                                ),
                                label=None
                            )
                        ],
                        documentation=None,
                        modifiers={'static', 'public'},
                        name='main',
                        parameters=[
                            FormalParameter(
                                annotations=[],
                                modifiers=set(),
                                name=args,
                                type=ReferenceType(
                                    arguments=None,
                                    dimensions=[None],
                                    name=String,
                                    sub_type=None
                                ),
                                varargs=False
                            )
                        ],
                        return_type=None,
                        throws=None,
                        type_parameters=None
                    )
                ],
                documentation=None,
                extends=None,
                implements=None,
                modifiers=set(),
                name='HelloWorldApp',
                type_parameters=None
            )
        ]
    )