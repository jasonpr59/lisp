#!/usr/bin/env python

import sys

import formatter
import interpreter
import parser
import tokenizer


def main(argv):
    file_name = argv[1]
    with open(file_name) as source_file:
        tokens = tokenizer.Tokenizer(source_file).get_tokens()

    # Are there useful ways to clean up a parse tree before we start
    # calling it an AST?
    # TODO(jasonpr): Investigate.
    for ast in parser.parse_trees(tokens):
        evaluation = interpreter.execute(ast)
        if evaluation is not None:
            print formatter.lisp_format(evaluation)

if __name__ == '__main__':
    main(sys.argv)
