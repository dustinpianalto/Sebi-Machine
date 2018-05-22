#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
IO stuff.
"""
import inspect
import os


__all__ = ('in_here',)


def in_here(*path_bits: str, stack_depth: int=0) -> str:
    """
    A somewhat voodooish and weird piece of code. This enables us to
    directly refer to a file in the same directory as the code that 
    calls this method, without any due regard for where in the file
    system tree it is.
    
    Apart from that, this will behave just like os.path.join, meaning
    that varaidic strings will be joined with the appropriate 
    directory separator for the current platform.
    
    This works by inspecting the stack frame for the caller.
    If you are planning on nesting this call in another utility and wish
    for the stack to refer to that caller, you should increment 
    the ``stack_depth`` arg for each nested call you make. By default,
    you can ignore this and it will default to 0.
    """
    try:
        frame = inspect.stack()[1 + nested_by]
    except IndexError:
        raise RuntimeError('Could not find a stack record. Interpreter has '
                           'been shot.')
    else:
        module = inspect.getmodule(frame[0])
        assert hasattr(module, '__file__'), 'No __file__ attr, whelp.'

        file = module.__file__

        dir_name = os.path.dirname(file)
        abs_dir_name = os.path.abspath(dir_name)

        return os.path.join(abs_dir_name, *paths)
 
