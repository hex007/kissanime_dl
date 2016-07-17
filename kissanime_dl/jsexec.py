# -*- coding: utf-8 -*-

import js2py


def cVunicode(any_a):
    try:
        return unicode(any_a, utf8)
    except NameError:
        return str(any_a)


def convJStoPy(string):
    string = cVunicode(string)
    return js2py.eval_js(string)
