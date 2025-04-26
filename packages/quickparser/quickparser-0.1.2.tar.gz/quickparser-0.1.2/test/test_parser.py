import pytest
import argparse
from unittest.mock import patch
from pydantic import BaseModel, Field
from pydantic_core import PydanticUndefined
from quickparser import parser_tools as pt
from typing import Union, Optional


class _TestModel(BaseModel):
    """
    Example model for testing.
    """
    name: str
    age: int = 30
    hobby: str | None
    favorite_color: str = pt.Field(default="blue", description="Favorite color")
    favorite_number: Optional[int] = pt.Field(default=None, description="Favorite number")
    is_strange: None | bool


@pytest.fixture
def fields():
    """
    Fixture to provide the fields of the TestModel.
    """
    return _TestModel.model_fields


def test_has_default(fields):
    """
    Test the _has_default function.
    """
    assert pt._has_default(fields["favorite_color"])
    assert pt._has_default(fields["age"])
    assert not pt._has_default(fields["hobby"])
    assert not pt._has_default(fields["name"])
    assert not pt._has_default(fields["favorite_number"])


def test_default_is_undefined(fields):
    """
    Test the _default_is_undefined function.
    """
    assert not pt._default_is_undefined(Field(default=42))
    assert pt._default_is_undefined(fields["hobby"])
    assert pt._default_is_undefined(fields["name"])
    assert not pt._default_is_undefined(fields["favorite_color"])
    assert not pt._default_is_undefined(fields["age"])
    assert not pt._default_is_undefined(fields["favorite_number"])


def test_get_type(fields):
    """
    Test the _get_type function.
    """
    assert pt._get_type(fields["hobby"]) == str
    assert pt._get_type(fields["name"]) == str
    assert pt._get_type(fields["age"]) == int
    assert pt._get_type(fields["favorite_color"]) == str
    assert pt._get_type(fields["favorite_number"]) == int
    assert pt._get_type(fields["is_strange"]) == None


def test_get_default(fields):
    """
    Test the _get_default function.
    """
    assert pt._get_default(fields["hobby"]) is None
    assert pt._get_default(fields["name"]) is None
    assert pt._get_default(fields["age"]) == 30
    assert pt._get_default(fields["favorite_color"]) == "blue"
    assert pt._get_default(fields["favorite_number"]) is None
    assert pt._get_default(fields["is_strange"]) is None


def test_field_is_explicitly_optional(fields):
    """
    Test the _field_is_explicitly_optional function.
    """
    assert pt._field_is_explicitly_optional(fields["hobby"])
    assert pt._field_is_explicitly_optional(fields["favorite_number"])
    assert not pt._field_is_explicitly_optional(Field(default=None))
    assert not pt._field_is_explicitly_optional(fields["name"])
    assert not pt._field_is_explicitly_optional(fields["age"])
    assert not pt._field_is_explicitly_optional(fields["favorite_color"])


def test_field_is_optional(fields):
    """
    Test the _field_is_optional function.
    """
    assert pt._field_is_optional(fields["hobby"])
    assert pt._field_is_optional(fields["favorite_number"])
    assert pt._field_is_optional(fields["age"])
    assert pt._field_is_optional(fields["favorite_color"])
    assert not pt._field_is_optional(Field(default=None))
    assert not pt._field_is_optional(fields["name"])


class TestParser:

    """
    Test the Parser class.
    """

    @pytest.fixture
    def argparser(self):
        """
        Fixture to provide the argument parser.
        """
        return pt.Parser._init_parser(_TestModel)


    @pytest.fixture
    def parser_cls(self, argparser):
        """
        Fixture to provide the parser class.
        """
        class _TestParser(pt.Parser):
            """
            Example parser for testing.
            """
            _parser = argparser
            _model = _TestModel
        return _TestParser
    
    @patch("sys.argv", new=["test_parser.py", "--name", "John", "--age", "25", "--is-strange"])
    def test_parser_class(self, parser_cls):
        """
        Test the parser class creation.
        """
        args = parser_cls.parse()
        assert args.name == "John"
        assert args.age == 25
        assert args.hobby is None
        assert args.favorite_color == "blue"
        assert args.favorite_number is None
        assert args.is_strange is True
        assert args.favorite_color == "blue"

    @patch("sys.argv", new=["test_parser.py", "--last-name", "Lee", "--first-name", "Perry", "--age", "15", "--is-strange"])
    def test_parser_class_from_args(self, parser_cls):
        @pt.parser
        class Person(BaseModel):
            last_name: str
            first_name: str
            age: int
            is_strange: None | bool

            @property
            def full_name(self):
                return f"{self.first_name} {self.last_name}"

        o = Person.from_args()
        assert o.first_name == "Perry"
        assert o.last_name == "Lee"
        assert o.age == 15
        assert o.full_name == "Perry Lee"
        assert o.is_strange is True

    def test_init_parser(self, parser_cls):
        """
        Test the _init_parser function.
        """
        parser = parser_cls._init_parser(parser_cls._model)
        assert isinstance(parser, argparse.ArgumentParser)


def test_parser_class_decorator():
    """
    Test the parser class creation.
    """
    parser = pt.parser(_TestModel)
    assert parser.__name__ == "_TestModel"
    assert issubclass(parser, pt.Parser)
    assert parser._model == _TestModel
    assert parser.__doc__ == _TestModel.__doc__
    assert parser.__module__ == _TestModel.__module__
