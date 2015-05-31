#!/usr/bin/env python

import sys

import tokenizer
import parser
import interpreter

def main(argv):
    file_name = argv[1]
    with open(file_name) as source_file:
        tokens = tokenizer.Tokenizer(source_file).get_tokens()

    # Are there useful ways to clean up a parse tree before we start
    # calling it an AST?
    # TODO(jasonpr): Investigate.
    for ast in parser.parse_trees(tokens):
        evaluation = interpreter.execute(ast)
            print evaluation
        if evaluation is not None:

if __name__ == '__main__':
    main(sys.argv)
