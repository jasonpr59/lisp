#!/usr/bin/env python

"""The main driver for the Lisp system."""

import sys

import environment
import formatter
import interpreter
import lexer
import parser
import pyfuncs


def _execute_file(code_file, env, print_results=False):
    """Execute some lisp.

    Args:
       code_file: An iterator over lines of Lisp text.
       env: The base environment.
       print_results: Whether to print the value of each top-level expression.
    """

    tokens = lexer.TokenSupply(lexer.lisp_tokens(code_file))
    # Are there useful ways to clean up a parse tree before we start
    # calling it an AST?
    # TODO(jasonpr): Investigate.
    for ast in parser.parse_trees(tokens):
        evaluation = interpreter.execute(ast, env)
        if print_results and evaluation is not None:
            print formatter.lisp_format(evaluation)

def _base_env():
    """Make a base environment.

    Contains functions implemented in Python, and functions defined
    as Lisp in standard libraries.
    """
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

def _line_reader():
    """Read and yield lines of Lisp text."""
    while True:
        yield raw_input('jlisp > ')

def main(argv):
    """Execute a Lisp script if provided, otherwise run a REPL."""
    base_env = _base_env()

    if len(argv) >= 2:
        file_name = argv[1]
        with open(file_name) as source_file:
            _execute_file(source_file, base_env, print_results=True)
    else:
        _execute_file(_line_reader(), base_env, print_results=True)

if __name__ == '__main__':
    main(sys.argv)
