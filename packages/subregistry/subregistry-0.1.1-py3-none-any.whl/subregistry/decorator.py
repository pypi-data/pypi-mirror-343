import logging
from functools import wraps

from .subclass_registry import SubclassRegistry


def add_registry(
        cls=None, *, registry_name: str = "registry", exclude_base: bool = True, warn_init_subclass: bool = True
    ):
    """Adds a registry to the target class.

    This registry works through the dunder method `__init_subclass__()`. If it is already defined by the class to which
    this decorator is applied, the existing implementation will still be called and the logic of this decorator will be
    executed afterwards.

    Args:
        registry_name: The name of the registry which will be exposed as a read-only class property. Note that an
            internal list called `__<registry_name>` will be defined. If any of these two conflict with existing
            attributes, a custom name for the registry can be specified.
        exclude_base: If True, the registry will not include the base class (i.e. the class to which this decorator is
            applied).
        warn_init_subclass: If True, this will warn the user that the class to which the registry is applied already
            defines an `__init_subclass__()` method. This is merely there to warn the user and make sure that the
            decorator will not interfere with the existing method. In most cases this won't be an issue and developpers
            can explicitely set `warn_init_subclass=False` to remove this warning.
    """

    def decorator(cls):
        # Print warning when decorator is first applied, has to be done this way to work both when decorator called with
        # or without parameters.
        if decorator._first_call:
            __check_registry_name(cls, registry_name)
            __check_init_subclass(cls, warn_init_subclass)
            decorator._first_call = False

        # Add registry and helper methods
        setattr(cls, registry_name, SubclassRegistry())
        if not exclude_base:
            getattr(cls, registry_name).register_class(cls)

        # Add book-keeping in __init_subclass__
        original_init_subclass = getattr(cls, "__init_subclass__")
        @wraps(original_init_subclass)
        def new_init_subclass(klass, **kwargs):
            if original_init_subclass:
                original_init_subclass(**kwargs)
            getattr(cls, registry_name).register_class(klass)
        setattr(cls, "__init_subclass__", classmethod(new_init_subclass))

        return cls
    decorator._first_call = True  # Init 'static' variable

    # If applied directly (@add_registry), cls is the class, otherwise return a decorator
    if cls is None or isinstance(cls, type):
        return decorator(cls) if cls else decorator
    else:
        raise TypeError("Unexpected argument passed to decorator")


def __check_init_subclass(cls, warn: bool):
    """Optionally warns if the class already defines __init_subclass__."""
    if warn and "__init_subclass__" in cls.__dict__:
        logging.warning(
            f"Class {cls.__name__} already defines '__init_subclass__()'. "
            "The logic of this decorator will be added at the end of it, but might interfere."
            "If you are confident this behavior is fine, consider specifying 'warn_init_subclass=False'."
        )


def __check_registry_name(cls, registry_name: str):
    """Raises a value error if the registry name is already defined in the class."""
    if hasattr(cls, registry_name):
        raise ValueError(
            f"Class {cls.__name__} already defines an attribute/function for '{registry_name}'. "
            "Consider specifying a different value for 'registry_name'."
        )
