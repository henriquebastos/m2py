#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import division

import os
import sys

from ipshellapi import Ipshell


from utils import resource_path
from subprocess import Popen
from Listener import Listener

ipsh = Ipshell()

#listener = Listener()

#pyserver.namespace = globals()
#listener.namespace = ipsh.user_ns

@ipsh.magic("values")
def list_values(self, arg):
    """
    List all numeric types
    """

    ipsh.get_magic(u'whos int float float64 ndarray')

@ipsh.magic("arrays")
def list_arrays(self, arg):
    """
    Show all ndarrays
    """

    ipsh.get_magic(u'whos ndarray list')

@ipsh.magic("lists")
def list_lists(self, arg):
    """
    Show all lists objects
    """
    ipsh.get_magic(u'whos list')

@ipsh.magic("strings")
def list_strings(self, arg):
    ipsh.get_magic(u'whos str')

@ipsh.magic("functions")
def list_functions(self, arg):
    ipsh.get_magic(u'whos function')

@ipsh.magic("addpath")
def addpath(self, path):
    """ Add path to sys.path """
    sys.path.append(path)

@ipsh.magic("digits")
def set_digits(self, args):
    """
    Set IPython Shell number of digits

    :param n: Maximum number of decimal places to be displayed
    :type  n: int
    :return:
    """

    try:
        n, type = args.split()
    except:
        print """
        $ digits #digits <format>

            Example:
            $ digits 5 fix

        """
    if type == 'fix':
        base = '.%sf'

    formt= '%' + base % n
    #get_ipython().magic('precision '+formt)
    ipsh.exec_magic('precision '+formt)


@ipsh.magic("see")
def see(self, args):
    """
    Explore Object members

    Usage:

        %see <type> <object>

        <type>

        a       : Print all object members
        f       : Print all object functions
        m       : Print all object modules
        c       : Print all classes defined in object
        file    : See which file the object is defined
        v       : Print all values (float, ndarray defined in module)

    Example:
    In [14]: import os
    In [15]: see f os
    _execvpe ._exists ._get_exports_list ._make_stat_result ...

    """

    import inspect

    try:
        type, obj = args.split()
        obj = eval(obj, ipsh.user_ns)
    except Exception as err:
        print \
        """
        Explore Object members

        Usage:

            %see <type> <object>

            <type>

            a       : Print all object members
            f       : Print all object functions
            m       : Print all object modules
            c       : Print all classes defined in object
            file    : See which file the object is defined
            v       : Print all values (float, ndarray defined in module)

        Example:
        In [14]: import os
        In [15]: see f os
        _execvpe ._exists ._get_exports_list ._make_stat_result ...
        """

        #print err
        return

    members = inspect.getmembers(obj)

    filter_member = lambda filterfunc: \
    [m[0] for m in members if filterfunc(m[1])]

    if type == "a":

        print " ".join([m[0] for m in members])

    elif type == "f":
        #funcs = [m[0] for m in members if inspect.isfunction(m[1])]
        funcs = filter_member(inspect.isfunction)
        print " .".join(funcs)

    elif type == "file":
        print inspect.getsourcefile(obj)

    elif type == "c":
        #classes = [m[0] for m in members if inspect.isclass(m[1])]
        classes = filter_member(inspect.isclass)
        print " .".join(classes)

    elif type == "m":
        #classes = [m[0] for m in members if inspect.isclass(m[1])]
        modules = filter_member(inspect.ismodule)
        print " ".join(modules)

    elif type == "v":
        #classes = [m[0] for m in members if inspect.isclass(m[1])]
        vfilter = lambda obj: isinstance(obj, float) or isinstance(obj, int)

        modules = filter_member(vfilter)
        print " ".join(modules)

@ipsh.magic("docs")
def __docs__(self, arg=""):

    if not arg:

        print \
        """
        Show PDF documentation

        Usage:
            Show available documentation
            $ docs list

            Open documentation
            $ docs <doctype>

            <doctype>
                quickref - Show Quick reference pdf
        """
        return

    if arg == "list":
        resourcedir = resource_path("resources")
        doclist = map( lambda f: f.split('.pdf')[0],  os.listdir(resourcedir))
        print " ".join(doclist)
        return

    filename = resource_path("resources/%s.pdf" % arg)
    print filename
    Popen("xdg-open %s > /dev/null 2>&1" % filename, shell=True)

@ipsh.magic("listener")
def __listener__(self, arg):

    if arg == "on":
        listener.start()

    elif arg == "off":
        listener.stop()

    else:
        print "Turn on/off remote listener server"
        print "%listener [on|off]"


@ipsh.magic("diary")
def diary(self, arg):
    """
    Matlab Diary Equivalent

    Save Command Window text to file
    expand all in page
    Syntax

    diary
    diary('filename')
    diary off
    diary on
    diary filename
    """

    if not arg:
        ipsh.exec_magic("logstart -o diary")

    elif arg == "off":
        ipsh.exec_magic("logstop")
    else:
        ipsh.exec_magic("logstart %s" % arg)







def __show_cheat_sheet__(self, arg):

    print """
    %<magic> [[args]]

    See PDF documentation
    ----------------------------------------------------------------
        docs <doctype>

        <doctype>
             quickref - Show Quick reference pdf

        Example:
            $ docs quickref

    Add Path to sys.path ( import path )
    ----------------------------------------------------------------
        $ addpath <path>

        Example:
        In [2]: %addpath /home/tux/PycharmProjects/m2py
        In [3]: import m2py as m

    Show Values
    ----------------------------------------------------------------

        Show all user variables
        $ whos

        Show all floats and ints
        $ values

        Show all ndarrays and lists
        $ arrays

        Show all functions
        $ functions

        Show all strings
        $ strings

    Explore Object members
    ----------------------------------------------------------------
    %see <type> <object>

    <type>

    a       : Print all object members
    f       : Print all object functions
    m       : Print all object modules
    c       : Print all classes defined in object
    file    : See which file the object is defined
    v       : Print all values (float, ndarray defined in module)



    """

__usage__ = \
"""
Enter:
    %usage       - to show usage
    %cheatsheet  - To show commands examples
    %magic       - To show Magic Functions User guide
    $quickref    - IPython quick reference card
"""

def __show_usage__(self, arg):
    print __usage__


@ipsh.magic("finance_mode")
def _finance_mode(self, arg):
    print "Loading Finance package"
    print "Objects: finance, factors, amortizacao"
    exec("from finance import *", ipsh.user_ns)

@ipsh.magic("thermo_mode")
def _thermo_mode(self, arg):
    print "Loading Thermodynamic package: xsteam, gas"
    print "to see details type: $ xsteam? or object?"
    exec("from thermo import *", ipsh.user_ns)




def main():
    # Set ipython to auto reload modules

    import units

    ipsh.autoreload()
    ipsh.autocall()

    ipsh.IP.banner1 =  __usage__
    ipsh.set_magic("usage", __show_usage__)
    ipsh.set_magic("cheatsheet", __show_cheat_sheet__)

    #listener.main()

    ipsh.load_modules(['units', 'numerical', 'constants', 'thermo'], hidden=True)
    
    ipsh.load_functions_from_module("numpy", [
        "array", "sin", "cos","log", "log10", "exp", "linspace", "logspace", "arange",
        "std", "var", "mean", "average", "cov", "corrcoef", "cumsum", "cumprod",
        "min", "max", "sum", "histogram",
    ], hidden=True)


    # ipsh.load_functions_from_module("extra", ["deg2rad", "rad2deg", "sind", "cosd", "tand", "arctan2d",
    #                                           "eng", "eng2"], hidden=True)

    import matplotlib.pyplot as plt
    ipsh.user_ns['plt'] = plt
    ipsh.ipsh.user_ns_hidden.add('plt')
    plt.ion()

    #ipsh.load_functions_from_module("matplotlib.pylab", ["ion", "plot", "show", "clf", "figure"], hidden=True)

    ipsh.run()

if __name__ == "__main__":
    main()


