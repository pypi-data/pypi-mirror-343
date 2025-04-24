from typing import override

from pygoerrors.protocols import Error


class NotSetType(Error):
    @override
    def __repr__(self) -> str:
        return "NotSet"

    def __bool__(self) -> bool:
        return False

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, NotSetType):
            return True

        return value is None

    @override
    def error(self) -> str:
        return ""


NotSet = NotSetType()
