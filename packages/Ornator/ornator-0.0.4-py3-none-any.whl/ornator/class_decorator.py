from typing import TypeVar
from functools import wraps
from typing import Type, Callable

T = TypeVar('T', bound=object)

class BaseClassDecorator:
    """Base class for all class decorators"""
    def __init__(self):
        self.__pre: Callable|None = None
        self.__pos: Callable|None = None

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


class BeforeClassDecorator(BaseClassDecorator):
    """Executes pre_handler before class instantiation"""
    def before(self, **decorator_kwargs):
        def class_decorator(cls: Type[T])->Type[T]:
            original_init = cls.__init__

            @wraps(original_init)
            def wrapped_init(instance, *args, **kwargs):
                if not self.pre:
                    raise ValueError("Missing pre function")
                pre_value = self.pre(cls, *args, **kwargs, **decorator_kwargs)
                setattr(instance, '_pre_value', pre_value)
                original_init(instance, *args, **kwargs)

            cls.__init__ = wrapped_init
            return cls
        return class_decorator


class AfterClassDecorator(BaseClassDecorator):
    """Modifies class after its definition"""
    def after(self, **decorator_kwargs):
        def class_decorator(cls: Type[T])->Type[T]:
            if not self.pos:
                raise ValueError("Missing pos function")
            
            return self.pos(cls, **decorator_kwargs)
        return class_decorator


class DualClassDecorator(BaseClassDecorator):
    """Executes pre_handler during instantiation and modifies class methods"""
    def dual(self, **decorator_kwargs):
        def class_decorator(cls: Type[T])->Type[T]:
            if not (self.pre and self.pos):
                raise ValueError("Missing pre or pos functions")

            original_init = cls.__init__

            @wraps(original_init)
            def wrapped_init(instance, *args, **kwargs):
                pre_value = self.pre(cls, *args, **kwargs, **decorator_kwargs)
                setattr(instance, '_pre_value', pre_value)
                original_init(instance, *args, **kwargs)

            cls.__init__ = wrapped_init
            self.pos(cls, **decorator_kwargs)
            return cls

        return class_decorator


class EmptyClassDecorator(BaseClassDecorator):
    """Allows custom class modification without restrictions"""
    def empty(self, handler: Callable = None, **decorator_kwargs):
        if handler and not callable(handler):
            raise TypeError(f"Expected callable handler, got {type(handler)}")

        def class_decorator(cls: Type[T])->Type[T]:
            if handler:
                return handler(cls, **decorator_kwargs)
            return cls

        return class_decorator
