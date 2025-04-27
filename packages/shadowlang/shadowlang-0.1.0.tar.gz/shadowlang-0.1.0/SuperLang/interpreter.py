from SuperLang.tokens import Integer, Float

class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base
        self.functions = {}

    def read_INT(self, value):
        return int(value)
    
    def read_FLT(self, value):
        return float(value)
    
    def read_VAR(self, id):
        variable = self.data.read(id)
        return getattr(self, f"read_{variable.type}")(variable.value)

    def compute_bin(self, left, op, right):
        left_val = self.interpret(left)
        right_val = self.interpret(right)

        if op.value == "add": return left_val + right_val
        elif op.value == "subtract": return left_val - right_val
        elif op.value == "multiply": return left_val * right_val
        elif op.value == "divide": return left_val / right_val
        elif op.value == "equals": return int(left_val == right_val)
        elif op.value == "greater": return int(left_val > right_val)
        elif op.value == "less": return int(left_val < right_val)
        elif op.value == "greater_or_equal": return int(left_val >= right_val)
        elif op.value == "less_or_equal": return int(left_val <= right_val)
        elif op.value == "and": return int(left_val and right_val)
        elif op.value == "or": return int(left_val or right_val)

    def compute_unary(self, operator, operand):
        operand_val = self.interpret(operand)
        if operator.value == "add": return +operand_val
        elif operator.value == "subtract": return -operand_val
        elif operator.value == "not": return int(not operand_val)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree
        
        if isinstance(tree, list):
            result = None
            for statement in tree:
                result = self.interpret_statement(statement)
            return result
        return self.interpret_statement(tree)
    
    def interpret_statement(self, statement):
        if isinstance(statement, dict) and statement["type"] == "function":
            self.functions[statement["name"]] = statement
            return None

        elif isinstance(statement, tuple):
            if statement[0] == "declare":
                _, var, expr = statement
                value = self.interpret(expr)
                self.data.write(var, value)
                return value
            
            elif statement[0] == "give":
                return self.interpret(statement[1])

        elif isinstance(statement, list):
            if len(statement) == 2:
                return self.compute_unary(statement[0], statement[1])
            else:
                return self.compute_bin(statement[0], statement[1], statement[2])

        elif hasattr(statement, 'type'):
            if statement.type == "VAR":
                return self.read_VAR(statement)
            elif statement.type in ["INT", "FLT"]:
                return getattr(self, f"read_{statement.type}")(statement.value)

        return statement