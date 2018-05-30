#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
IO stuff.
"""
import copy
import inspect
import os


__all__ = ('in_here',)


def in_here(first_path_bit: str, *path_bits: str, stack_depth: int=0) -> str:
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
    
    :param first_path_bit: the initial path bit to operate with. This is 
        required.
    :param path_bits: additional bits of path to construct relative to here.
        These are entirely optional.
    :param stack_depth: optional, defaults to 0. How many nested calls
        we expect this to be called in. Affects the relative directory
        that is used.
    :returns: the absolute path to the given relative path provided.
    """    
    try:
        frame = inspect.stack()[1 + stack_depth]
    except IndexError:
        raise RuntimeError('Could not find a stack record. Interpreter has '
                           'been shot.')
    else:
        module = inspect.getmodule(frame[0])        
        assert hasattr(module, '__file__'), 'No `__file__\' attr, welp.'
        
        # https://docs.python.org/3/library/inspect.html#the-interpreter-stack
        # If Python caches strings rather than copying when we move them
        # around or modify them, then this may cause a referential cycle which
        # will consume more memory and stop the garbage collection system
        # from working correctly. Best thing to do here is deepcopy anything
        # we need and prevent this occuring. Del the references to allow them
        # to be freed.
        file = module.__file__
        file = copy.deepcopy(file)
        del module, frame
        dir_name = os.path.dirname(file)
        abs_dir_name = os.path.abspath(dir_name)
        pathish = os.path.join(abs_dir_name, first_path_bit, *path_bits)
        return pathish
