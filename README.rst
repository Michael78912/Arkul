=====
Arkul
=====

-------------------------------------------
Arkul: A tool for more flexible HTML pages.
-------------------------------------------

.. contents::

About
=====

Arkul gives you a way to define constants, read large datas from files,
and obtain dynamic input from python scripts (on compile time)

Example (from examples/example.arkl)
====================================

.. code-block::

    # define Greeting to be equal to "Hello"
    %define Greeting "Hello"
    # give the metadata. will be compiled to <meta> tags.
    %metadata {charset: "utf-8", version: 0.1}
    # define Msg1 to the contents of file "examples/message1.txt"
    %define Msg1 @load("examples\message1.txt")

    # import python's standard "time" module
    %import time

    # define the html section with attributes lang.
    html with ( lang = "en" ) {
        # do the head section. <meta> tags are not needed
        # since we used the metadata command.
        head {
            title {Greeting}
        }
        # define the body section
        body {
            # access the contents of Greeting and use it
            h1 {Greeting}
            p {
                # access Msg1 and use it
                Msg1
            }
            p {
                # read message2.txt and use the contents
                @load("examples\message2.txt")
            }
            p {
                # use the time module's "asctime" function to print
                # the time at which it was compiled.
                "Compiled at: " @asctime()
            }
        }
    }

Usage
=====

to compile this to html, type :code:`python -m arkul <yourfilehere>.arkl`


Installation
============

have to figure this out yet. for now, just clone the repository
:code:`git clone https://github.com/Michael78912/Arkul`, then use as a module.

Commands
========

Currently, only three commands exist. metadata, import, and define.

A command starts with the symbol "%", followed by the name, then arguments.

meta(data)
~~~~~~~~~~

syntax: :code:`%meta(data) {attribute: value (, attribute: value)*}`

this is just a nicer way of applying <meta> tags. instead of

.. code-block::

    head {
        meta with ( charset="utf-b" ) {}
    }

you could do just
    :code:`%meta {charset: "utf-8}`


define
~~~~~~

syntax: :code:`%define IDENTIFIER VALUE`

IDENTIFIER must be a valid identifier (match :code:`/[a-zA-Z_][a-zA-Z0-9_]*/`)




