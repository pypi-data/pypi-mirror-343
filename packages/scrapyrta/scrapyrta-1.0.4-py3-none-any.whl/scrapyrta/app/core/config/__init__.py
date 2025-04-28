from copy import deepcopy
from importlib import import_module

from . import default_settings


class Settings:
    def __init__(self):
        self.setmodule(default_settings)

    def setmodule(self, module):
        if isinstance(module, str):
            module = import_module(module)

        for setting in dir(module):
            if setting.startswith("_") or not setting.isupper():
                continue

            self.set(setting, getattr(module, setting))

    def __setattr__(self, key, value):
        if self.frozen:
            raise TypeError("Trying to modify a frozen Settings object")

        return super().__setattr__(key, value)

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as e:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'"
            ) from e

    def set(self, name, value):
        if not name.startswith("_") and name.isupper():
            # Deepcopy objects here, or we will have issues with mutability,
            # like changing mutable object stored in settings leads to
            # change of object in default_settings module.
            setattr(self, name, deepcopy(value))

    def freeze(self):
        self._frozen = True

    def __str__(self) -> str:
        attrs = {
            key: getattr(self, key)
            for key in dir(self)
            if key.isupper() and not key.startswith("_")
        }

        formatted = "\n".join(f"{key}: {value}" for key, value in attrs.items())
        return f"{self.PROJECT_NAME} Settings:\n\n{formatted}\n"

    @property
    def frozen(self):
        return bool(getattr(self, "_frozen", False))


app_settings = Settings()
