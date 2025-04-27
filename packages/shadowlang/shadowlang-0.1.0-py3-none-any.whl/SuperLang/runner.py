import sys
from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data

def run_file(filename):
    with open(filename, 'r') as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    data = Data()
    interpreter = Interpreter(tree, data)
    interpreter.interpret()

def main():
    if len(sys.argv) < 2:
        print("Usage: shadow <file.shadow>")
        sys.exit(1)

    filename = sys.argv[1]
    run_file(filename)

if __name__ == "__main__":
    main()
