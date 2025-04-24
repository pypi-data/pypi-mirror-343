from functools import wraps
from typing import Any, Callable, Optional

class BaseDecorator:
    """Base class for all decorators"""
    def __init__(self):
        self.__pre: Optional[Callable[..., Any]] = None
        self.__pos: Optional[Callable[..., Any]] = None

    @property
    def pre(self):
        return self.__pre

    @pre.setter
    def pre(self, value):
        if not callable(value):
            raise TypeError(f"Expected callable, got {type(value)}")
        self.__pre = value

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        if not callable(value):
            raise TypeError(f"Expected callable, got {type(value)}")
        self.__pos = value


class BeforeDecorator(BaseDecorator):
    """Executes pre_handler before the function"""
    def before(self, **decorator_kwargs):
        def outer_decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if not self.pre:
                    raise ValueError("Missing pre function")
                pre_value = self.pre(*args, **kwargs, **decorator_kwargs)
                kwargs.pop('pre', None)
                return function(pre=pre_value, *args, **kwargs)
            return wrapper
        return outer_decorator


class AfterDecorator(BaseDecorator):
    """Executes pos_handler after the function"""
    def after(self, **decorator_kwargs):
        def outer_decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if not self.pos:
                    raise ValueError("Missing pos function")
                result = function(*args, **kwargs)
                return self.pos(result, **decorator_kwargs)
            return wrapper
        return outer_decorator


class DualDecorator(BaseDecorator):
    """Executes pre_handler before and pos_handler after the function"""
    def dual(self, **decorator_kwargs):
        def outer_decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if not (self.pre and self.pos):
                    raise ValueError("Missing pre or pos functions")
                pre_value = self.pre(*args, **kwargs, **decorator_kwargs)
                kwargs.pop('pre', None)
                result = function(pre=pre_value, *args, **kwargs)
                return self.pos(result, **decorator_kwargs)
            return wrapper
        return outer_decorator


class EmptyDecorator(BaseDecorator):
    """Allows custom function handling without pre/pos restrictions"""
    def empty(self, handler: Callable[..., Any] = None, **decorator_kwargs):
        if handler and not callable(handler):
            raise TypeError(f"Expected callable handler, got {type(handler)}")
            
        def outer_decorator(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if handler:
                    return handler(function, *args, **kwargs, **decorator_kwargs)
                return function(*args, **kwargs)
            return wrapper
        return outer_decorator
