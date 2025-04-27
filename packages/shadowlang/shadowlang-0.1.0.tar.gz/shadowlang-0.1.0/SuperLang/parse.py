from SuperLang.tokens import Integer, Float, Reserved

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]

    def factor(self):
        if self.token.type in ["INT", "FLT"]:
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolean_expression()
            self.move()
            return expression
        elif self.token.value == "not":
            operator = self.token
            self.move()
            return [operator, self.boolean_expression()]
        elif self.token.type == "VAR":
            return self.token
        elif self.token.value in ["add", "subtract"]:
            operator = self.token
            self.move()
            return [operator, self.boolean_expression()]

    def term(self):
        left_node = self.factor()
        self.move()
        
        while self.token.value in ["multiply", "divide"]:
            operator = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node, operator, right_node]

        return left_node

    def expression(self):
        left_node = self.term()
        while self.token.value in ["add", "subtract"]:
            operator = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operator, right_node]

        return left_node

    def comp_expression(self):
        left_node = self.expression()
        if self.token.type == "COMP":
            operator = self.token
            self.move()
            right_node = self.expression()
            return [left_node, operator, right_node]
        return left_node

    def boolean_expression(self):
        left_node = self.comp_expression()
        while self.token.value in ["and", "or"]:
            operator = self.token
            self.move()
            right_node = self.comp_expression()
            left_node = [left_node, operator, right_node]
        return left_node

    def parse(self):
        statements = []
        while self.idx < len(self.tokens):
            if self.token.type == "FUNC":
                statements.append(self.parse_function())
            else:
                statements.append(self.statement())
            if self.idx < len(self.tokens):
                self.move()
        return statements

    def parse_function(self):
        self.move()
        name = self.token.value
        self.move()
        self.move()
        
        params = []
        while self.token.value != ")":
            params.append(self.token.value)
            self.move()
            if self.token.value == ",":
                self.move()
        
        self.move()
        body = []
        while self.token.value != "end":
            body.append(self.statement())
            self.move()
        
        return {"type": "function", "name": name, "params": params, "body": body}

    def statement(self):
        if self.token.type == "DECL":
            self.move()
            var = self.token
            self.move()
            if self.token.value == "=":
                self.move()
                expr = self.boolean_expression()
                return ("declare", var, expr)
        
        elif self.token.value == "give":
            self.move()
            return ("give", self.boolean_expression())
        
        return self.boolean_expression()

    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]