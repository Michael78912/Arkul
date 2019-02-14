"""common.py- 
basic functions to be used during the compilation
of Arkul files. you can specify additional files to be loaded
by using the %import command.
"""

import urllib.request

def load(filename):
    """read the file and return the contents."""
    with open(filename) as file:
        return file.read()

def fetch(url):
    """download the url and return the contents."""
    with urllin.request.urlopen(url) as file:
        return file.read()
