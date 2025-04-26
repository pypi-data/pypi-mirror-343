from functools import wraps
from typing import Any, Callable, Generic, Optional, ParamSpec, Tuple, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class DecoratorInjector(Generic[T]):


    def __init__(self, *decorators:Tuple[Callable[P, T]]):
        self.__decorators = decorators


    def _getattr_wrapper(self, func:Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        def wrapper(instance:object, name:str) -> T:
            attr = func(instance, name)
            if callable(attr):
                for decorator in self.__decorators:
                    attr = decorator(attr)
            return attr
        return wrapper


    def __call__(self, cls:type[T]) -> T:
        cls.__getattribute__ = self._getattr_wrapper(cls.__getattribute__)
        return cls
