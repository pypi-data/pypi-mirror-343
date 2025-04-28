import inspect
import numbers
from collections.abc import Mapping
from typing import Union, final, Any, TypeVar, Tuple, List

import numpy as np
from numpy.typing import ArrayLike

from .modules import get_module_version
if get_module_version('python') >= (3, 9, 0):
    from collections.abc import (
        Iterable,
        Mapping,
        MutableMapping,
        Generator,
    )
else:
    from typing import (
        Iterable,
        Mapping,
        MutableMapping,
        Generator,
    )

__all__ = ["Numeric", "Scalar", "Real", "ArrayLike", "NOTSET", "NOTSETTYPE", "T",
           "Iterable", "Mapping", "MutableMapping", "Generator",
           "is_container", "is_hashable", "is_iterable", "is_class",
           "is_function", "is_indexable_sequence"]

Numeric = Union[int, float]

Scalar = Numeric

Real = numbers.Real

ArrayType = Union[np.ndarray, List[float], Tuple[float, ...]]

ArrayContainer = Union[Tuple[ArrayLike, ...], List[ArrayLike], np.ndarray]

@final
class NOTSETTYPE:
    """A type used as a sentinel for unspecified values."""
    
    def __copy__(self):
        return self
        
    def __deepcopy__(self, memo: Any):
        return self

NOTSET = NOTSETTYPE()

T = TypeVar('T')

def is_container(obj: Any) -> bool:
    return hasattr(obj, '__contains__')

def is_hashable(obj: Any) -> bool:
    return hasattr(obj, '__hash__')

def is_iterable(obj: Any) -> bool:
    return hasattr(obj, '__iter__')

def is_class(obj: Any) -> bool:
    return inspect.isclass(obj)

def is_function(obj: Any) -> bool:
    return inspect.isfunction(obj)

def is_lambda(obj: Any) -> bool:
    return inspect.isfunction(obj) and obj.__name__ == "<lambda>"

def is_indexable_sequence(obj: Any) -> bool:
    """
    Return True if `obj` behaves like a sequence (supports iteration, indexing, and len())
    but is NOT a mapping, string, bytes, set, or generator.

    This will catch things like:
      - list, tuple
      - numpy.ndarray
      - custom sequence types implementing __iter__, __getitem__, and __len__

    And will exclude:
      - dict or other Mapping
      - str, bytes
      - set
      - generators, iterators without __len__ or __getitem__

    Parameters
    ----------
    obj : Any
        The object to test.

    Returns
    -------
    bool
        True if `obj` is a pure indexable sequence; False otherwise.
    """
    return (
        hasattr(obj, '__iter__')
        and hasattr(obj, '__getitem__')
        and hasattr(obj, '__len__')
        and not isinstance(obj, (str, bytes, Mapping))
    )