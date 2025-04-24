from __future__ import annotations

from collections.abc import Iterable
from typing import override

from pygoerrors.helpers import NotSet, NotSetType
from pygoerrors.protocols import Error, WrappedError


def new(message: str) -> Error:
    return stringError(message)


def _is(err: Error, target: Error) -> bool:
    while True:
        if err == target:
            return True

        if isinstance(err, WrappedError):
            err = err.unwrap()
            if not err:
                return False
        else:
            return False


def is_(err: Error, target: Error) -> bool:
    if not err or not target:
        return err == target

    return _is(err, target)


def as_[T: Error](err: Error, target: type[T]) -> T | NotSetType:
    if not err:
        return NotSet

    while True:
        if isinstance(err, target):
            return err

        if isinstance(err, WrappedError):
            err = err.unwrap()
            if not err:
                return NotSet
        else:
            return NotSet


def join(*errs: Error) -> Error:
    filtered_errors = filter(lambda e: e, errs)
    errors = list(filtered_errors)

    if len(errors) == 0:
        return NotSet

    return jsonError(errors)


class stringError(Error):
    def __init__(self, error: str):
        self.__error = error

    @override
    def error(self) -> str:
        return self.__error


class jsonError(Error):
    def __init__(self, errs: Iterable[Error]):
        self.__errs = errs

    @override
    def error(self) -> str:
        return "\n".join(map(lambda e: e.error(), self.__errs))


class wrappedError(Error, WrappedError):
    def __init__(self, msg: str, error: Error):
        self.__message = msg
        self.__error = error

    @override
    def unwrap(self) -> Error:
        return self.__error

    @override
    def error(self) -> str:
        return self.__message
