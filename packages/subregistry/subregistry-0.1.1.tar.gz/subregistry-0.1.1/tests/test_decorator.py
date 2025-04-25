import logging

import pytest

from subregistry import add_registry


def test_add_registry():

    @add_registry
    class Test:
        pass

    assert hasattr(Test, "registry")
    assert Test.registry.registry == tuple()


def test_add_registry_custom_name():

    @add_registry(registry_name="custom")
    class Test:
        pass

    assert hasattr(Test, "custom")
    assert Test.custom.registry == tuple()


def test_add_registry_include_base():

    @add_registry(exclude_base=False)
    class Test:
        pass

    assert hasattr(Test, "registry")
    assert Test.registry.registry == (Test,)


def test_warn_init_subclass(caplog):

    with caplog.at_level(logging.WARNING):
        @add_registry
        class Test:
            def __init_subclass__(cls):
                pass  # Warn me!

        assert "already defines '__init_subclass__()'" in caplog.text


def test_registry_name_error():

    with pytest.raises(ValueError):
        @add_registry
        class Test:
            registry = object()


def test_register_classes():

    @add_registry
    class Test:
        pass

    class X(Test):
        pass

    class Y(Test):
        pass

    class Z(Y):
        pass

    assert Test.registry.registry == (X, Y, Z)


def test_register_on_import():
    from tests.classes import Base, A, B, C

    assert Base.registry.registry == (A, B, C)
