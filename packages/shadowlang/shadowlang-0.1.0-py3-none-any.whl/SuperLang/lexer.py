from SuperLang.tokens import Integer, Float, Operation, Declaration, Variable, Boolean, Comparison, Reserved, Function

class Lexer:
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "()="
    stopwords = [" ", "\n", "\t"]
    declarations = ["set"]
    boolean = ["and", "or", "not"]
    comparisons = ["equals", "greater", "less", "greater_or_equal", "less_or_equal"]
    reserved = ["if", "else", "while", "fn", "give", "add", "subtract", 
               "multiply", "divide"]

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None
    
    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()
            
            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    if word == "fn":
                        self.token = Function(word)
                    else:
                        self.token = Reserved(word)
                elif word in Lexer.comparisons:
                    self.token = Comparison(word)
                else:
                    self.token = Variable(word)
            
            if self.token:
                self.tokens.append(self.token)
            self.token = None
        
        return self.tokens

    def extract_number(self):
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()
        
        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()
            if self.char == "_":
                word += self.char
                self.move()
        
        return word
    
    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]