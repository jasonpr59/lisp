#!/usr/bin/env python

import sys

import environment
import formatter
import interpreter
import parser
import pyfuncs
import tokenizer


def _execute_file(code_file, env, print_results=False):
    tokens = tokenizer.Tokenizer(code_file).get_tokens()
    # Are there useful ways to clean up a parse tree before we start
    # calling it an AST?
    # TODO(jasonpr): Investigate.
    for ast in parser.parse_trees(tokens):
        evaluation = interpreter.execute(ast, env)
        if print_results and evaluation is not None:
            print formatter.lisp_format(evaluation)

def _base_env():
    env = environment.Environment()

    # Provide some builtin functions, written in Python.
    for name, value in pyfuncs.functions.items():
        env[name] = value

    # Provide some functions, written in Lisp.
    BASE_LIB_FILENAMES = ['lib/builtin.lisp']
    for lib_filename in BASE_LIB_FILENAMES:
        with open(lib_filename) as lib_file:
            _execute_file(lib_file, env)

    return env

def main(argv):
    base_env = _base_env()

    file_name = argv[1]
    with open(file_name) as source_file:
        _execute_file(source_file, base_env, print_results=True)


if __name__ == '__main__':
    main(sys.argv)
