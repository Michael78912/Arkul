import importlib
import sys
import os

from lark import Lark, Transformer, exceptions

from . import common
from .compile_error import CompileError
from .htmlbuilder import Tag

SYNTAX_ERROR = """
            ({lineno}) {line}
                {arrow}
Syntax Error: unexpected character in "{file}" (line {lineno}, column {column})
"""


TEMPLATE = """<!DOCTYPE HTML>
<!--
HTML file. compiled from Arkul. ({filename})
original source : 

{source}

if you see an issue with the way this compiled, please start an issue at
https://github.com/Michael78912/Arkul/issues/new.
-->

{html}

<!-- By the way, Howdy! -->
"""

def main(ifile, ofile='out.html', template=True):
    parser = Lark(open(os.path.join(os.path.dirname(__file__), "Grammar.lark")).read())
    data = open(ifile).read()

    print('parsing file...')

    try:
        tree = parser.parse(data)
    except exceptions.UnexpectedCharacters as e:
        syntaxerror(ifile, data, e)
        print('parsing failed.')
        raise SystemExit(1)
    print('finished parsing')

    transformer = ArkulTransformer()

    try:
        transformer.transform(tree)
    except CompileError as e:
        print(e.get_message(), file=sys.stderr)
        print('compilation failed')
        raise SystemExit(1)

    root = Tag(transformer.firsttag)
    head = {tag if tag.name == 'head' else None for tag in root.contents}
    head.remove(None)
    head = list(head)[0]

    for key, value in zip(transformer.meta.keys(), transformer.meta.values()):
        head.add(['meta', {key: value}])

    data = TEMPLATE.format(
        filename=ifile,
        source=data,
        html=str(root),
    ) if template else str(root)

    with open(ofile, 'w') as openfile:
        openfile.write(data)
    
    print('compilation completed. ({})'.format(os.path.realpath(ofile)))

def syntaxerror(filename, file, exception):
    line = file.split('\n')[exception.line - 1]
    string = SYNTAX_ERROR.format(
        line=line,
        file=filename,
        lineno=exception.line,
        column=exception.column,
        arrow=" " * (exception.column - 1) + "^"
    )
    print(string, file=sys.stderr)

class ArkulTransformer(Transformer):
    """ a transformer object just for the Arkul language."""

    modules = [common]
    constants = {}
    firsttag = None
    meta = {}

    with_stmt = lambda _, tokens: tokens[1]
    number = lambda _, tokens: float(tokens[0])
    string = lambda _, tokens: tokens[0][1:-1]
    assignment = lambda _, tokens: {tokens[0]: tokens[1]}
    store_const = lambda _, tokens: tokens[0]
    identifier = lambda _, tokens: str(tokens[0])

    object = dict
    pair = tuple

    def metadata(self, tokens):
        """add the metadata."""
        self.meta = tokens[1]
    
    def import_stmt(self, tokens):
        """add a module to the list."""
        self.modules.append(importlib.import_module(tokens[1].split('.')[0]))

    def constant(self, tokens):
        """try and find a constant. if it is not defined, then raise an error."""
        try:
            return self.constants[tokens[0]]
        except KeyError:
            raise CompileError("constant %s not found!" % tokens[0])

    def define(self, tokens):
        """define a constant."""
        self.constants[tokens[1]] = tokens[2]

    def function(self, tokens):
        """find and use a function."""
        modules = []
        for module in self.modules:
            item = getattr(module, tokens[0], None)
            if item is not None:
                modules.append(item)

        if not modules:
            raise CompileError('function %s not found!' % tokens[0])
        elif len(modules) > 1:
            raise CompileError("more than 1 instances of {} found (in {})".format(
                tokens[0], [func.__module__ for func in modules]
            ))

        return modules[0](*tokens[1:])

    def tag(self, tokens):
        """add a tag to the list of tags"""
        # the first tag will be the last tag processed.
        self.firsttag = tokens
        return tokens


