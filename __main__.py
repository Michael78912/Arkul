"""__main__.py
run the compiler given the options it needs.
"""

import argparse
try:
    from __init__ import __version__ as _VER
except ImportError:
    from . import __version__ as _VER

from . import compiler


def main():
    parser = argparse.ArgumentParser(description="compile Arkul to html")
    parser.add_argument('file', help="arkul file to be compiled")
    parser.add_argument('-o', '--output', help="output file name", default='out.html')
    parser.add_argument('-n', '--no-template', action='store_true', help="don't use the default template")
    parser.add_argument('-v', '--version', action='version', version=_VER)
    namespace = parser.parse_args()
    compiler.main(namespace.file, namespace.output, not namespace.no_template)

if __name__ == "__main__":
    main()
