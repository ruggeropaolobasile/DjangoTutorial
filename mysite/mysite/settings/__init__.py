import importlib
import os
from types import ModuleType


def _resolve_settings_module() -> str:
    environment = os.getenv("DJANGO_ENV", "").strip().lower()
    if environment == "production":
        return "mysite.settings.production"
    if environment == "local":
        return "mysite.settings.local"
    return "mysite.settings.base"


def _load_settings_module() -> ModuleType:
    module = importlib.import_module(_resolve_settings_module())
    return importlib.reload(module)


_active_module = _load_settings_module()
for _name in dir(_active_module):
    if _name.isupper():
        globals()[_name] = getattr(_active_module, _name)
