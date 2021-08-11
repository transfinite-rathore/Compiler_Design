import Sansam.Lexer.Lexer
import Sansam.Values.Number
import Sansam.Parser.Parser
import Sansam.Interpreter.Interpreter
import Sansam.Context
import Sansam.Interpreter.SymbolTable as st

global_symbol_table = st.SymbolTable()
global_symbol_table.set("लुप्तः", Sansam.Values.Number.null)
global_symbol_table.set("असत्यम्", Sansam.Values.Number.false)
global_symbol_table.set("सत्यम्", Sansam.Values.Number.true)


def run(fn, text):
    # Generate tokens
    lexer = Sansam.Lexer.Lexer.Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    #print(tokens)
    if error:
        return None, error

    # Generate AST
    parser = Sansam.Parser.Parser.Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Sansam.Interpreter.Interpreter.Interpreter()
    context = Sansam.Context.Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

