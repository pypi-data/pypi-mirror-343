import logging


logger = logging.getLogger(__file__)


class SubclassRegistry:

    def __init__(self):
        self._registry = []

    @property
    def registry(self) -> tuple[type]:
        return tuple(self._registry)

    def register_class(self, klass: type):
        self._registry.append(klass)

    def get_by_name(self, name: str) -> type:
        """Returns a model class from the registry given its name."""

        for klass in self.registry:
            if klass.__name__ == name:
                return klass

        raise ValueError(f"Class '{name}' not found in registry.")
