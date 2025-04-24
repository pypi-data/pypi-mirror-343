#!/usr/bin/env python3
"""

"""

# Imports:
from __future__ import annotations

# ##-- stdlib imports
import datetime
import enum
import functools as ftz
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import string
import time
import types
import weakref
from uuid import UUID, uuid1

# ##-- end stdlib imports

# ##-- 1st party imports
from jgdv._abstract.protocols import SpecStruct_p, Buildable_p
from jgdv.structs.strang import CodeReference

from .core.meta import DKey
from .core.base import DKeyBase
from .keys import SingleDKey, MultiDKey, NonDKey
from ._interface import Key_p, DKeyMark_e
# ##-- end 1st party imports

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, Generic, cast, assert_type, assert_never
# Protocols:
from typing import Protocol, runtime_checkable
# Typing Decorators:
from typing import no_type_check, final, override, overload

if TYPE_CHECKING:
    from jgdv import Maybe, Ident, RxStr, Rx
    from typing import Final
    from typing import ClassVar, Any, LiteralString
    from typing import Never, Self, Literal
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

# isort: on
# ##-- end types

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class ArgsDKey(SingleDKey, mark=DKeyMark_e.ARGS):
    """ A Key representing the action spec's args """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._expansion_type  = list
        self._typecheck = list

    def expand(self, *sources, **kwargs) -> list:
        """ args are simple, just get the first specstruct's args value """
        for source in sources:
            if not isinstance(source, SpecStruct_p):
                continue

            return source.args
        else:
            return []

class KwargsDKey(SingleDKey, mark=DKeyMark_e.KWARGS):
    """ A Key representing all of an action spec's kwargs """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._expansion_type  = dict
        self._typecheck = dict

    def expand(self, *sources, fallback=None, **kwargs) -> dict:
        """ kwargs are easy, just get the first specstruct's kwargs value """
        for source in sources:
            if not isinstance(source, SpecStruct_p):
                continue

            return source.kwargs
        else:
            return fallback or {}
