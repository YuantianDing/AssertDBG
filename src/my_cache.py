
import hashlib
import json
from pydantic import BaseModel
import inspect
import os

def hash_dict_no_order(dictionary):
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    return hashlib.md5(encoded).hexdigest()

def my_cache(cache_dir: str):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    def decorator(func):
        def cached_func(*args, **kwargs):
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            input_dict = {}
            for k, v in bound.arguments.items():
                if isinstance(v, BaseModel):
                    input_dict[k] = v.model_dump()
                else:
                    input_dict[k] = v

            input_hash = hash_dict_no_order(input_dict)
            cache_file = os.path.join(cache_dir, f"{func.__name__}({input_hash}).json")
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    result = json.load(f)
                    bound = sig.bind(**result["in"])
                    bound.apply_defaults()
                    assert dict(bound.arguments) == input_dict
                    return func.__annotations__["return"].model_validate(result["out"])

            result = func(*args, **kwargs)
            assert isinstance(result, BaseModel)
            with open(cache_file, "w") as f:
                json.dump({"in": input_dict, "out": result.model_dump()}, f)
                return result
        return cached_func
    return decorator