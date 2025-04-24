from .decorators import to_errors, to_errors_iterable
from .errors import as_, is_, join, new
from .format import errorf
from .helpers import NotSet
from .protocols import Error

__all__ = [
    # types
    "Error",
    "NotSet",
    # core
    "new",
    "is_",
    "as_",
    "join",
    "errorf",
    # decorators
    "to_errors",
    "to_errors_iterable",
]
