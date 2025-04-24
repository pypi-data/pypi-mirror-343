from collections.abc import Iterable, Iterator
from typing import override

from pygoerrors.errors import new
from pygoerrors.helpers import NotSet
from pygoerrors.protocols import Error


class ErrorIterable[T: object](Iterable[T]):
    def __init__(self, iterable: Iterable[T]):
        self.__iterator = iterable.__iter__()
        self.__error: Error = NotSet

    @override
    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        if self.__error is not NotSet:
            raise StopIteration

        try:
            return self.__iterator.__next__()
        except StopIteration:
            raise
        except Exception as e:
            self.__error = new(str(e))
            raise StopIteration

    def err(self) -> Error:
        return self.__error
