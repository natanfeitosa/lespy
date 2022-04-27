from os import PathLike
from pathlib import Path
import typing as t

def python_file_for_dict(path: t.Union[str, PathLike, Path]) -> t.Dict[str, t.Any]:
    obj = dict()
    
    if not isinstance(path, Path):
        path = Path(path)
    
    out = {}
    exec(path.read_text(), out)

    for k, v in out.items():
        if k != '__builtins__':
            if type(v).__name__ == 'function':
                try:
                    v = v()
                except:
                    continue
            obj[k] = v
    return obj
