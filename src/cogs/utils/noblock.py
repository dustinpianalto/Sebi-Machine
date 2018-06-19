#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import asyncio
import functools


def no_block(func):
    """Turns a blocking function into a non-blocking coroutine function."""
    @functools.wraps(func)
    async def no_blocking_handler(*args, **kwargs):
        partial = functools.partial(func, *args, **kwargs)
        return await asyncio.get_event_loop().run_in_executor(None, partial)
    return no_blocking_handler
