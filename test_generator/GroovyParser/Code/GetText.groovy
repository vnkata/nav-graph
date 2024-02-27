package mypackage

import org.codehaus.groovy.ast.ASTNode
import org.codehaus.groovy.ast.builder.AstBuilder
import org.codehaus.groovy.ast.stmt.AssertStatement
import org.codehaus.groovy.ast.stmt.BlockStatement
import org.codehaus.groovy.ast.stmt.BreakStatement
import org.codehaus.groovy.ast.stmt.CaseStatement
import org.codehaus.groovy.ast.stmt.CatchStatement
import org.codehaus.groovy.ast.stmt.ContinueStatement
import org.codehaus.groovy.ast.stmt.DoWhileStatement
import org.codehaus.groovy.ast.stmt.EmptyStatement
import org.codehaus.groovy.ast.stmt.ExpressionStatement
import org.codehaus.groovy.ast.stmt.ForStatement
import org.codehaus.groovy.ast.stmt.IfStatement
import org.codehaus.groovy.ast.stmt.ReturnStatement
import org.codehaus.groovy.ast.stmt.SwitchStatement
import org.codehaus.groovy.ast.stmt.SynchronizedStatement
import org.codehaus.groovy.ast.stmt.ThrowStatement
import org.codehaus.groovy.ast.stmt.TryCatchStatement
import org.codehaus.groovy.ast.stmt.WhileStatement

import org.codehaus.groovy.ast.expr.Expression
import org.codehaus.groovy.ast.expr.ArrayExpression
import org.codehaus.groovy.ast.expr.ArgumentListExpression
import org.codehaus.groovy.ast.expr.BinaryExpression
import org.codehaus.groovy.ast.expr.BitwiseNegationExpression
import org.codehaus.groovy.ast.expr.BooleanExpression
import org.codehaus.groovy.ast.expr.CastExpression
import org.codehaus.groovy.ast.expr.ClassExpression
import org.codehaus.groovy.ast.expr.ClosureExpression
import org.codehaus.groovy.ast.expr.ConstantExpression
import org.codehaus.groovy.ast.expr.ConstructorCallExpression
import org.codehaus.groovy.ast.expr.DeclarationExpression
import org.codehaus.groovy.ast.expr.EmptyExpression
import org.codehaus.groovy.ast.expr.FieldExpression
import org.codehaus.groovy.ast.expr.GStringExpression
import org.codehaus.groovy.ast.expr.ListExpression
// import org.codehaus.groovy.ast.expr.ListOfExpressionsExpression
import org.codehaus.groovy.ast.expr.MapEntryExpression
import org.codehaus.groovy.ast.expr.MapExpression
import org.codehaus.groovy.ast.expr.MethodCallExpression
import org.codehaus.groovy.ast.expr.MethodPointerExpression
import org.codehaus.groovy.ast.expr.PostfixExpression
import org.codehaus.groovy.ast.expr.PrefixExpression
import org.codehaus.groovy.ast.expr.PropertyExpression
import org.codehaus.groovy.ast.expr.RangeExpression
import org.codehaus.groovy.ast.expr.SpreadExpression
import org.codehaus.groovy.ast.expr.SpreadMapExpression
import org.codehaus.groovy.ast.expr.StaticMethodCallExpression
import org.codehaus.groovy.ast.expr.TernaryExpression
import org.codehaus.groovy.ast.expr.TupleExpression
import org.codehaus.groovy.ast.expr.UnaryMinusExpression
import org.codehaus.groovy.ast.expr.UnaryPlusExpression
import org.codehaus.groovy.ast.expr.VariableExpression
import org.codehaus.groovy.ast.expr.ClosureListExpression

import org.codehaus.groovy.ast.Parameter

import mypackage.Identifier
import mypackage.Variable
import mypackage.Constant
import mypackage.Statement

"""
    getText function used to end recursive visitNode function and return a Identifier
    based on type of expression
"""
class TextGetter {
    // [x]
    public static Identifier getText(Expression exp) {
        println("[GetText] We have missed")
        println(exp)
        println(exp.getText())
        return Identifier()
    }

    public static Constant getText(ConstantExpression exp) {
        if (exp.getText() == 'null')
            return new Constant(value: 'null', datatype: '')
        return new Constant(value: exp.getText(), datatype: exp.getType())
    }

    public static Constant getText(ClassExpression exp) {
        return new Constant(value: "", datatype: exp.getText())
    }

    public static Constant getText(Object obj) {
        if (obj.getClass().getPackage().getName() != 'java.lang')
            println("We missed type: " + obj.getClass())
        return new Constant (value: obj, datatype: obj.getClass())
    }

    public static Constant getText(MapExpression exp) {
        return new Constant(value: exp.getText(), datatype: "map")
    }

    public static Variable getText(Parameter p) {
        return new Variable(name: p.getName(), datatype: p.getType())
    }

    public static Variable getText(VariableExpression exp) {
        return new Variable(name: exp.getText(), datatype: exp.getType())
    }

    public static Variable getText(PropertyExpression exp) {
        return new Variable(name: exp.getText(), datatype: "")
    }

    public static Statement getText(BooleanExpression exp) {
        return new Statement(code: exp.getText())
    }

    public static Statement getText(ClosureListExpression exp) {
        return new Statement(code: exp.getText())
    }

    public static Statement getText(ListExpression exp){
        return new Statement(code: exp.getText())
    }

    public static Statement getText(ArrayExpression exp){
        def code = 'new '
        code += exp.getElementType()
        def dim = exp.getSizeExpression()

        for (def d : dim) {
            code += '[' + d.getValue().toString() + ']'
        }
        return new Statement(code: code)
    }

    public static Statement getText(BinaryExpression exp){
        return new Statement(code: TextGetter.getString(exp))
    }

    public static Statement getText(PostfixExpression exp){ 
        return new Statement(code: exp.getText())
    }
    
    public static Statement getText(PrefixExpression exp){ 
        return new Statement(code: exp.getText())
    }
    
    public static Statement getText(ConstructorCallExpression exp){
        return new Statement(code: exp.getText())
    }

    public static ArrayList<Identifier> getText(ArgumentListExpression exp) {
        def args = exp.getExpressions()
		def ArrayList<Identifier> strArgs = new ArrayList<Identifier>()
        for (Expression expression : args){
            strArgs.add(TextGetter.getText(expression))
        }
        return strArgs
    }

    public static Statement getText(MethodCallExpression exp) {
        def res = ''
        def receiver = TextGetter.getString(exp.getReceiver())
		def method = exp.getMethodAsString()
        def args = exp.getArguments()
        if (receiver) {
            res += receiver + '.'
        }
		args = TextGetter.getString(args)
        res += method + "(" + args + ")"
        println("[GetText.getText]: method call " + res )
        // return new Statement(code: exp.getText())
        return new Statement(code: res)
    }

    public static String getString(Expression exp) {
        print("[GetText.getString]: this should not be printed: ")
        println(exp)
        return exp.getText()
    }

    public static String getString(Constant exp){
        println("[getString Constant]" + exp.getType())
        if (exp.getType() == "String")
            return "'" + exp.getText() + "'"
        else
            return exp.getText()
    }

    public static String getString(ArgumentListExpression exp) {
        def res = ''
        for (Expression arg : exp) {
            def tmp = TextGetter.getString(arg)
            res += tmp + ', '
        }
        println("[GET STRING]: " + res)
        return res.dropRight(2)
    }

    public static String getString(VariableExpression exp) {
        return exp.getText()
    }

    public static String getString(ConstantExpression exp) {
        println("GetString " + exp.getType())
        if (exp.getType().getText() == 'java.lang.String')
            return "'" + exp.getText() + "'"
        else 
            return exp.getText()
    }

    public static String getString(BinaryExpression exp) {
        def code = ''
        code += TextGetter.getString(exp.getLeftExpression()) + ' ' + exp.getOperation().getText() + ' ' + TextGetter.getString(exp.getRightExpression())
    }

}


