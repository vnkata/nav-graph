package mypackage

import org.codehaus.groovy.ast.ASTNode
import org.codehaus.groovy.ast.builder.AstBuilder
import org.codehaus.groovy.ast.stmt.Statement
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

import mypackage.TextGetter
import mypackage.State

class NodeVisitor {
    private static AstBuilder builder = new AstBuilder()
    private static String[] specialOps = ['+=', '-=', '*=', '/=', '>>=', '<<=', '&=', '|=']

	static def visitNode(Statement stmt) {
        println("Visit statement: " + stmt.toString())
    }

    ///.
	static def visitNode(AssertStatement stmt) {
        println("Visit Assert Statement")
		def assertion = TextGetter.getText(stmt.getBooleanExpression())
		def mess = TextGetter.getText(stmt.getMessageExpression())
        def result = new State(action: "assert")
        result.setInput(assertion)
        if (mess != null)
            result.setOutput(mess)
        return result
    }

    ///.
	static def visitNode(BlockStatement stmt) {
        println("Visit block statement")
        // println(stmt)
		def result = new ArrayList<State>()
        if (!stmt.isEmpty()){
    		def inside = stmt.getStatements()
            for (Statement statement : inside){
        		def tmp = visitNode(statement)
                // println("******************")
                // print("Statement: ")
                // println(statement)
                // print("Visit: ")
                // println(tmp)
                if (tmp instanceof List)
                    result.addAll(tmp)
                else 
                    result.add(tmp)
                // println("*******************")
            }
        }
        // println(result)
        return result
    }

    ///.
	static def visitNode(BreakStatement stmt) {
        println("Visit Break Statement")     
        return new State(action: "Break")
    }

    ///.
	static def visitNode(CaseStatement stmt) {
        println("Visit Case Statement")     
		def cond = TextGetter.getText(stmt.getExpression())

		def result = new State(action: "Case")
        result.setInput(cond)

		def child = visitNode(stmt.getCode())
        result.setChild(child)
        return result 
    }

    ///.   
	static def visitNode(CatchStatement stmt) {
        println("Visit Catch Statement")    
        def input = TextGetter.getText(stmt.getVariable()) 
        def code = visitNode(stmt.getCode())
        def result = new State(action: "Catch")
        result.setInput(input)
        result.setChild(code)
        return result
    }

    ///.
	static def visitNode(ContinueStatement stmt) {
        println("Visit Continue Statement")     
        return new State(action: "Continue")
    }
        
    ///.
	static def visitNode(DoWhileStatement stmt) {
        println("Visit Do WhileStatement")     
		def cond = TextGetter.getText(stmt.getBooleanExpression())		
        def child = visitNode(stmt.getLoopBlock())
		def result = new State(action: "Do while")
        result.setInput(cond)
        if (child) {
            result.setChild(child)
        }
        return result 
    }

    ///.
	static def visitNode(EmptyStatement stmt) {    
        println("Visit Empty Statement")     
        return null
    }

    ///.
	static def visitNode(ExpressionStatement stmt) {
        println("Visit Epxression Statement")
        return visitNode(stmt.getExpression())
    } 

    ///.
	static def visitNode(ForStatement stmt) {
        println("Visit For Statement") 
        // println(stmt.getCollectionExpression())
		def cond = TextGetter.getText(stmt.getCollectionExpression())
		def child = visitNode(stmt.getLoopBlock())
		def result = new State(action: "For")
        result.setInput(cond)
        // print("[Debug for statement child]: ")
        // println(child)
        result.setChild(child)
        return result
    }

    ///.
	static def visitNode(IfStatement stmt) {
        println("Visit If Statement")     
		def cond = TextGetter.getText(stmt.getBooleanExpression())
		def child = visitNode(stmt.getIfBlock())
		def ifState = new State(action: 'If')
        ifState.setInput(cond)
        ifState.setChild(child)

		def elseState = new State(action: 'Else')
		def elseChild = visitNode(stmt.getElseBlock())
        
        if (elseChild)
            elseState.setChild(elseChild)
        return new ArrayList<State>([ifState, elseState])
    }

    ///.
	static def visitNode(ReturnStatement stmt) {
        println("Visit Return Statement")
        if (!stmt.isReturningNullOrVoid())
            return visitNode(stmt.getExpression())
        else
            return null
    }

    ///.
	static def visitNode(SwitchStatement stmt) {
        println("Visit Switch Statement")    
        // println(stmt.getExpression()) 
		def swit = TextGetter.getText(stmt.getExpression())
		def cases = stmt.getCaseStatements()
		def result = new State(action: "Switch", input: swit)
        
		def child = new ArrayList<State>()
        for (def cas : cases) {
            child.add(visitNode(cas))
        }

		def defaultCase = visitNode(stmt.getDefaultStatement())
        def defaultState = new State(action: "Default")
        defaultState.setChild(defaultCase)
        child.add(defaultState)

        result.setChild(child)
        return result
    }
        
	static def visitNode(SynchronizedStatement stmt) {
        println("Visit Synchronized Statement")     
        println("Not implemented")
        println(stmt)

    }
    
    ///.
	static def visitNode(ThrowStatement stmt) {
        println("Visit Throw Statement")     
        def except = TextGetter.getText(stmt.getExpression())
        def result = new State(action: "Throw") 
        result.setInput(except)
        return result
    }
        
    ///.
	static def visitNode(TryCatchStatement stmt) {
        println("Visit Try Catch Statement")     
		def insideTry = visitNode(stmt.getTryStatement())
        def tryBlock = new State(action: "Try")
        tryBlock.setChild(insideTry)
        // println("==========================================")
        // println("==========================================")

		def catches = stmt.getCatchStatements()
		def catchesBlocks = new ArrayList<State>()
        for (def ca : catches) {
            catchesBlocks.add(visitNode(ca))
        }

		def finallyBlock = visitNode(stmt.getFinallyStatement())
        def finallyState = new State(action: "Finally")
        finallyState.setChild(finallyBlock)
        println("=====================================")
        println(stmt.getFinallyStatement())
        println("=====================================")
		def result = new ArrayList<State>()
        result.addAll(tryBlock)
        result.addAll(catchesBlocks)
        if (finallyState)
            result.addAll(finallyState)
        // println("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        // println(result)
        return result
    }
    
    ///.
	static def visitNode(WhileStatement stmt) {
        println("Visit While Statement")     
		def cond = TextGetter.getText(stmt.getBooleanExpression())
		def child = visitNode(stmt.getLoopBlock())
		def result = new State(action: 'While')
        result.setInput(cond)
        result.setChild(child)
        return result

    }
        
	static def visitNode(Expression exp) {
        println("Visit expression: " + exp.toString())
    }

    ///. 
	static def visitNode(ArrayExpression exp) {
        println("Visit Array Expression") 
		// def dim = exp.getSizeExpression()
		// def result = new ArrayList<String>()
        // for (def x : dim) {
        //     result.add(TextGetter.getText(x))
        // }
        // return new State("", "assignment", [result], "")
        def inp = TextGetter.getText(exp)
        def result = new State(action: "Assignment")
        result.setInput(inp)
        return result
    }

    ///.
	static def visitNode(ArgumentListExpression exp) {
        println("Visit Argument List Expression")
		def args = exp.getExpressions()
		def ArrayList<String> strArgs = new ArrayList<String>()
        for (Expression expression : args){
            println("AAAAAAAAA")
            strArgs.add(TextGetter.getString(expression))
        }
        return strArgs
    }

    // TODO: Working on it
	static def visitNode(BinaryExpression exp) {
        println("Visit Binary Expression")     
        // println("Not so sure about Binary Expresssion")
        
        def op = exp.getOperation().getText()
        if (op == '='){
            def result = null
            if (exp.getRightExpression() instanceof BinaryExpression)
                result = new State(action: "Assignment", input: TextGetter.getText(exp.getRightExpression()))
            else 
                result = visitNode(exp.getRightExpression())
            result.setOutput(TextGetter.getText(exp.getLeftExpression()))
            return result
        }
        else if (specialOps.contains(op)) {
            // println("This is correct")
            String rewrite = ""
            String var = exp.getLeftExpression().getText()
            op = op[0..-2]
            rewrite += var + " = " + var + " " + op + " "+ exp.getRightExpression().getText()
            println("Debug: " + rewrite)
            def node = builder.buildFromString(rewrite)
            // println(node)
            return visitNode(node[0])[0]
        }
        else if (op[-1] != '='){
            def result = visitNode(exp.getRightExpression())
            result.setOutput(TextGetter.getText(exp.getLeftExpression()))
            return result
        }
        else{
            println("We missed in Binary Expression with operator " + op)
        }
    }
        
	static def visitNode(BitwiseNegationExpression exp) {
        println("Visit Bitwise NegationExpression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(BooleanExpression exp) {
        println("Visit Boolean Expression")     
        println("Not implemented")
        println(exp)

    }
        
    // def visitNode(BytecodeExpression exp) {
    //     println("Visit Bytecode Expression")     
    //     println("Not implemented")
    //     println(exp)
    // }
        
	static def visitNode(CastExpression exp) {
        println("Visit Cast Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(ClassExpression exp) {
        println("Visit Class Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(ClosureExpression exp) {
        println("Visit Closure Expression")     
        println("Not implemented")
        println(exp)
    }
        
    ///.
	static def visitNode(ConstantExpression exp) {
        println("Visit Constant Expression")
        def result = new State(action: "Assignment")
        result.setInput(TextGetter.getText(exp.getValue()))
        return result
    }
        
	static def visitNode(ConstructorCallExpression exp) {
        println("Visit Constructor Call Expression")
        // println(exp.getText())     
        def result = new State(action: "Assignment")
        def inp = TextGetter.getText(exp)
        result.setInput(inp)
        return result
    }
        
	static def visitNode(DeclarationExpression exp) {
        println("Visit Declaration Expression");
        
        def lhs = TextGetter.getText(exp.getVariableExpression())
        def rhs = visitNode(exp.getRightExpression())
        
        rhs.setOutput(lhs)
        // def vars = new ArrayList<String>()
        // for (def e : lhs) {
        //     vars += TextGetter.getText(e)
        // }
        
        // for (def e : rhs) {
        //     println("+++++++++++++++++++++++++++++++")
        //     println(e)
        //     println("+++++++++++++++++++++++++++++++")
        //     exps.add(visitNode(e))
        // }
        
        // for (int i = 0; i < exps.size(); ++i)
        //     if (exps[i])
        //         exps[i].setOutput(vars[i])

        return rhs
    }

	static def visitNode(EmptyExpression exp) {
        println("Visit Empty Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(FieldExpression exp) {
        println("Visit Field Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(GStringExpression exp) {
        println("Visit G StringExpression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(ListExpression exp) {
        println("Visit List Expression")     
        def result = new State(action: "Assignment")
        result.setInput(TextGetter.getText(exp))
        return result
    }
        
    // def visitNode(ListOfExpressionsExpression exp) {
    //     println("Visit List OfExpressionsExpression")     
    //     println("Not implemented")
    //     println(exp)
    // }
        
	static def visitNode(MapEntryExpression exp) {
        println("Visit Map EntryExpression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(MapExpression exp) {
        println("Visit Map Expression")     
        println("Not implemented")
        println(exp)

    }
        
    ///.
	static def visitNode(MethodCallExpression exp) {
        println("Visit Method Call Expression")     
		def receiver = visitNode(exp.getReceiver())
		def method = exp.getMethodAsString()
		def args = TextGetter.getText(exp.getArguments())

        // println("=======================================================")
        // println(receiver)
        // println(method)
        // println(args)
        // println("=======================================================")
        return new State(receiver: receiver, action: method, input: args)
    }
        
	static def visitNode(MethodPointerExpression exp) {
        println("Visit Method Pointer Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(PostfixExpression exp) {
        println("Visit Postfix Expression")     
        def result = new State(action: "Statement")
        result.setInput(TextGetter.getText(exp))
        return result

    }
        
	static def visitNode(PrefixExpression exp) {
        println("Visit Prefix Expression")     
        def result = new State(action: "Statement")
        result.setInput(TextGetter.getText(exp))
        return result
    }
        
	static def visitNode(PropertyExpression exp) {
        println("Visit Property Expression")     
        println("Not implemented")
        println(exp)
    }
        
	static def visitNode(RangeExpression exp) {
        println("Visit Range Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(SpreadExpression exp) {
        println("Visit Spread Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(SpreadMapExpression exp) {
        println("Visit Spread MapExpression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(StaticMethodCallExpression exp) {
        println("Visit Static MethodCallExpression")     
        println("Not implemented")
        println(exp)

    }
            
	static def visitNode(TernaryExpression exp) {
        println("Visit Ternary Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(TupleExpression exp) {
        println("Visit Tuple Expression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(UnaryMinusExpression exp) {
        println("Visit Unary MinusExpression")     
        println("Not implemented")
        println(exp)

    }
        
	static def visitNode(UnaryPlusExpression exp) {
        println("Visit Unary PlusExpression")     
        println("Not implemented")
        println(exp)
    }

    // Wrong format
	static def visitNode(VariableExpression exp) {
        println("Visit Variable Expression") 
        println(exp)    
        return exp.getName()
    }
}
