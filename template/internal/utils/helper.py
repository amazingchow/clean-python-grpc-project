# -*- coding: utf-8 -*-
import time
from functools import wraps

from loguru import logger as loguru_logger


def cost_count(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        t = f(*args, **kwargs)
        loguru_logger.debug(f"{f.__name__} took time: {time.time() - start:.3f} secs.")
        return t
    return wrapper
