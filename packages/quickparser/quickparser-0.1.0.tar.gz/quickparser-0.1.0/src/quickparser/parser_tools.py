import sys
from typing import TypeVar, Generic, Union
from functools import wraps

UnionType = Union
is_ge_310 = False
if sys.version_info >= (3, 10):
    is_ge_310 = True
    from types import UnionType

import argparse
from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefinedType
from pydantic.fields import FieldInfo

T = TypeVar('T', bound=type[BaseModel])


class Parser(Generic[T]):

    _model: T = None
    _parser: argparse.ArgumentParser = None


    @classmethod
    def _init_parser(cls, model: T) -> argparse.ArgumentParser:
        """
        Initialize the argument parser.
        """
        parser = argparse.ArgumentParser(description=model.__doc__)
        for field_name, field in model.model_fields.items():
            is_optional = _field_is_optional(field)
            _type = _get_type(field)
            default = _get_default(field)
            parser.add_argument(
                f'--{field_name}',
                type=_type,
                default=default,
                required=not is_optional,
                help=field.description or ''
            )
        return parser

    @classmethod
    def parse(cls):
        """
        Parse the command line arguments.
        """
        return cls._parser.parse_args()


def parser(cls=None, **kwargs) -> Parser[T]:
    """
    Decorator to create a parser for a Pydantic model.
    """
    def decorator(cls: T) -> Parser[T]:
        @wraps(cls)
        def wrapper(**kwargs) -> Parser[T]:
            argparser = Parser._init_parser(cls)
            return type(cls.__name__, (Parser,), {
                '_model': cls,
                '_parser': argparser,
                '__doc__': cls.__doc__,
                '__module__': cls.__module__,
            })
        return wrapper(**kwargs)
    if cls is None:
        return decorator
    return decorator(cls)


def _field_is_optional(field: Field) -> bool:
    """
    Check if a field is optional.
    """
    return any([
        _field_is_explicitly_optional(field),
        _has_default(field),
        (_field_is_explicitly_optional(field) and _default_is_undefined(field))
    ])


def _field_is_explicitly_optional(field: FieldInfo) -> bool:
    """
    Check if a field is explicitly optional.
    """

    is_typing_union = (
        hasattr(field.annotation, '__origin__') and
        field.annotation.__origin__ is Union
    )

    if not is_ge_310:
        return (
            field.annotation is not None and 
            is_typing_union and
            type(None) in field.annotation.__args__
        )

    else:
        return (
            field.annotation is not None and
            (isinstance(field.annotation, UnionType) or is_typing_union) and
            type(None) in field.annotation.__args__ 
        )

def _get_type(field: FieldInfo) -> type:
    """
    Get the type of a field.
    """
    if _field_is_explicitly_optional(field):
        _type = field.annotation.__args__[0]
        if _type is type(None):
            _type = field.annotation.__args__[1]
    else:
        if isinstance(field.annotation, type):
            _type = field.annotation
        else:
            _type = None
    return _type


def _get_default(field: FieldInfo) -> object:
    """
    Get the default value of a field.
    """
    if _has_default(field):
        return field.default
    return None

def _has_default(field: FieldInfo) -> bool:
    """
    Check if a field has a default value.
    """
    return field.default is not None and not isinstance(field.default, PydanticUndefinedType)

def _default_is_undefined(field: FieldInfo) -> bool:
    """
    Check if a field's default value is undefined.
    """
    return isinstance(field.default, PydanticUndefinedType)