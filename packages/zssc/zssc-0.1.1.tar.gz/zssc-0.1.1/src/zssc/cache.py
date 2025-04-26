import json
import os
import os.path as osp
from functools import wraps
from typing import Callable, TypeVar, Union

T = TypeVar("T")


def cache(
    func: Union[Callable[..., T], None] = None,
    *,
    cache_path: str,
) -> Callable[..., T]:
    """Wrap a function to cache its result.

    Args:
        cache_path (str): The path to the cache file.
        func (Union[Callable[..., T], None], optional): The function to wrap. Defaults to None.

    Returns:
        Callable[..., T]: The wrapped function.

    Usage:
        ```python
        # 1. As function
        cached_f = cache(func, cache_path="tmp/res.json")
        out = cached_f(*args, **kwargs)

        # 2. As decorator
        @cache(cache_path="tmp/res.json")
        def func(...): ...
        ```
    """
    assert cache_path.endswith(".json"), "`cache_path` must end with .json"

    if func is None:  # * decorator syntax
        return lambda f: cache(f, cache_path=cache_path)

    @wraps(func)
    def wrapper(*args, **kwargs):
        if osp.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        else:
            result = func(*args, **kwargs)
            dir_path = osp.dirname(cache_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(cache_path, "w") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            return result

    return wrapper
