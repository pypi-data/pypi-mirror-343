import functools
from collections.abc import Iterable
from typing import Callable, cast

from pygoerrors.errors import new
from pygoerrors.helpers import NotSet
from pygoerrors.iterators import ErrorIterable
from pygoerrors.protocols import Error


def to_errors[T: object, **P](func: Callable[P, T]) -> Callable[P, tuple[T, Error]]:
    @functools.wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> tuple[T, Error]:
        try:
            return func(*args, **kwargs), NotSet
        except Exception as e:
            return cast(T, None), new(str(e))

    return wrapped


def to_errors_iterable[T: object, **P](
    func: Callable[P, Iterable[T]],
) -> Callable[P, ErrorIterable[T]]:
    @functools.wraps(func)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> ErrorIterable[T]:
        return ErrorIterable(func(*args, **kwargs))

    return wrapped
