import pytest

from subregistry.subclass_registry import SubclassRegistry

from tests.classes import Base, A, B, C


def test_instantiate():
    registry = SubclassRegistry()
    assert registry._registry == []


def test_get_by_name():
    registry = SubclassRegistry()
    registry._registry.append(Base)

    assert registry.get_by_name("Base") == Base


def test_get_by_name_error():
    registry = SubclassRegistry()

    with pytest.raises(ValueError):
        registry.get_by_name("Base") == Base


def test_register_class():
    registry = SubclassRegistry()
    registry._registry.append(A)


def test_registry():
    registry = SubclassRegistry()
    registry._registry.append(A)
    registry._registry.append(B)
    registry._registry.append(C)

    assert isinstance(registry.registry, tuple)
    assert registry.registry == (A, B, C)
