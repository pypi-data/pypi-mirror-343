import os
from collections.abc import Callable, Iterator
from typing import TypeVar

from environ import Env

_T = TypeVar("_T")


def _walk_to_root(path: str) -> Iterator[str]:
    """
    Yield directories starting from the given directory up to the root
    """

    if not os.path.exists(path):
        raise OSError("Starting path not found")

    if os.path.isfile(path):
        path = os.path.dirname(path)

    last_dir = None
    current_dir = os.path.abspath(path)
    while last_dir != current_dir:
        yield current_dir
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        last_dir, current_dir = current_dir, parent_dir


def find_dotenv(filename: str = ".env") -> str | None:
    path = os.getcwd()

    for dirname in _walk_to_root(path):
        check_path = os.path.join(dirname, filename)
        if os.path.isfile(check_path):
            return check_path


def get_env(name: str, default: _T, type_func: Callable) -> _T:
    return type_func(f"{PROJECT_NAME.upper()}_{name}", default=default)


env = Env()
env.read_env(env_file=find_dotenv())

PROJECT_NAME = "ScrapyRTA"

DEBUG = get_env("DEBUG", default=False, type_func=env.bool)
LOG_LEVEL = get_env("LOG_LEVEL", default="INFO", type_func=env.str)
ENABLE_OPEN_API = get_env("ENABLE_OPEN_API", default=True, type_func=env.bool)

PROJECT_SETTINGS = None

TIMEOUT_LIMIT = get_env("TIMEOUT_LIMIT", default=30, type_func=env.int)  # seconds
