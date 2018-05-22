#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
Neko404NotFound 2018, MIT

A mixin class that injects a suitably named logger into class scope
at runtime.

Chosen to make this a slotted class, which means (as far as I can remember)
that it is not suitable to be made into an abc.ABC class. Slots will
enable derived slotted classes to be a bit more efficient at runtime and
boast faster lookups.
"""
import logging


__all__ = ('Loggable',)


class Loggable:
    __slots__ = ('logger',)
    
    def __init_subclass__(cls, **_):
        cls.logger = logging.getLogger(cls.__qualname__)
