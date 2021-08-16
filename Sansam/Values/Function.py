import Sansam.Values.Value as val
import Sansam.Interpreter.RunTimeResult as rtr
import Sansam.Interpreter.Interpreter as it
import Sansam.Context as ct
import Sansam.Interpreter.SymbolTable as st
import Sansam.Error.Errors as error
import Sansam.Values.Number as num

class Function(val.Value):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__()
        self.name = name or "<Anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = rtr.RunTimeResult()
        interpreter = it.Interpreter()
        new_context = ct.Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = st.SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(error.RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))

        if len(args) < len(self.arg_names):
            return res.failure(error.RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too few args passed into '{self.name}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.should_return() and res.func_return_value is None:
            return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or num.null

        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"