stmt_pre = 'import org.codehaus.groovy.ast.stmt.'
exp_pre = 'import org.codehaus.groovy.ast.expr.'

def process(name):
    for i, c in enumerate(name):
        if 'A' <= c <='Z' and i != 0:
            return name[:i], name[i:]
    return name, ""


def generateClass(name):
    id = "stmt" if 'Statement' in name else "exp"
    a, b = process(name)
    return """
def visitNode({0} {1}) [
    println("Visit {2} {3}")     
    println("Not implemented")
]
    """.format(name, id, a, b)

def header(file):
    file.write("""
import org.codehaus.groovy.ast.ASTNode
import org.codehaus.groovy.ast.builder.AstBuilder
import org.codehaus.groovy.ast.expr.Expression
import org.codehaus.groovy.ast.stmt.Statement
""")

def import_template(classes, import_pre, file):
    for name in classes:
        file.write(import_pre + name + '\n')

statements = ["Statement", "AssertStatement", "BlockStatement", "BreakStatement", "CaseStatement", "CatchStatement", "ContinueStatement", "DoWhileStatement", "EmptyStatement", "ExpressionStatement", "ForStatement", "IfStatement", "ReturnStatement", "SwitchStatement", "SynchronizedStatement", "ThrowStatement", "TryCatchStatement", "WhileStatement"]
expressions = ["Expression", "ArrayExpression", "BinaryExpression", "BitwiseNegationExpression", "BooleanExpression", "BytecodeExpression", "CastExpression", "ClassExpression", "ClosureExpression", "ConstantExpression", "ConstructorCallExpression", "EmptyExpression", "FieldExpression", "GStringExpression", "ListExpression", "ListOfExpressionsExpression", "MapEntryExpression", "MapExpression", "MethodCallExpression", "MethodPointerExpression", "PostfixExpression", "PrefixExpression", "PropertyExpression", "RangeExpression", "SpreadExpression", "SpreadMapExpression", "StaticMethodCallExpression", "TemporaryVariableExpression", "TernaryExpression", "TupleExpression", "UnaryMinusExpression", "UnaryPlusExpression", "VariableExpression"]
with open("template.groovy", "w+") as file:
    header(file)
    import_template(statements, stmt_pre, file)
    file.write('\n')
    import_template(expressions, exp_pre, file)

with open("template.groovy", "a") as file:
    for name in statements:
        file.write(generateClass(name))
    for name in expressions:
        file.write(generateClass(name))
