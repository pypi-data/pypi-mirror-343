# subregistry

Utility Python library to easily create registries of sub-classes and import them conveniently.

## Installation

```bash
pip install subregistry
```

## Usage

To add a registry to a class, simply import and use the decorator:

```python
from subregistry import add_registry

@add_registry
class BaseClass:
    pass
```

Any **Imported** subclass of `BaseClass` will then automatically be registered.

Registered subclasses can later be retrieved by name as follows:

```python
BaseClass.registry.get_by_name("SubClass")
```

See the `examples` folder for more in-depth usages.

## Author

* Thomas Havy
