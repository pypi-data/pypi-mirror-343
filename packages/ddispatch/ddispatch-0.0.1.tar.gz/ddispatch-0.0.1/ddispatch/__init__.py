import inspect

from functools import singledispatch
from typing import overload, TYPE_CHECKING


if TYPE_CHECKING:
    dispatch = overload
else:

    def dispatch(f):
        """Decorator for creating generic functions"""
        crnt = inspect.currentframe()
        outer = crnt.f_back

        if f.__name__ not in outer.f_locals:
            generic = singledispatch(f)
            generic._is_singledispatch = True

            # overwrite the behavior of defaulting to the initial
            # function, then register it explicitly so its first argument
            # type is used.
            generic.register(object, _raise_not_implemented)
            generic.register(f)
            return generic
        else:
            generic = outer.f_locals[f.__name__]
            if not getattr(generic, "_is_singledispatch"):
                raise ValueError(
                    f"Function {f.__name__} does not appear to be a generic function"
                )

            generic.register(f)

            return generic


def _raise_not_implemented(dispatch_on):
    raise TypeError(f"No dispatch implementation for type: {type(dispatch_on)}")
