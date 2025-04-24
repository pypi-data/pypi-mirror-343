#!/usr/bin/env python3
"""

"""

# Imports:
from __future__ import annotations

# ##-- stdlib imports
import builtins
import datetime
import enum
import functools as ftz
import importlib
import itertools as itz
import logging as logmod
import pathlib as pl
import re
import time
import types
import typing
import weakref
from uuid import UUID, uuid1

# ##-- end stdlib imports

# ##-- 1st party imports
from jgdv.mixins.annotate import SubAnnotate_m
from jgdv.structs.chainguard import ChainGuard

# ##-- end 1st party imports

from jgdv.cli.errors import ArgParseError
from ._base import ParamSpecBase
from .core import LiteralParam, ToggleParam, RepeatToggleParam

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType, Any
# Protocols:
from typing import Protocol, runtime_checkable
# Typing Decorators:
from typing import no_type_check, final, override, overload

if TYPE_CHECKING:
    from jgdv import Maybe
    from typing import Final
    from typing import ClassVar, Any, LiteralString
    from typing import Never, Self, Literal
    from typing import TypeGuard
    from collections.abc import Iterable, Iterator, Callable, Generator
    from collections.abc import Sequence, Mapping, MutableMapping, Hashable

##--|
from .._interface import ParamStruct_p
# isort: on
# ##-- end types
##-- logging
logging = logmod.getLogger(__name__)
##-- end logging


class HelpParam(ToggleParam): #[bool]):
    """ The --help flag that is always available """

    def __init__(self, **kwargs):
        kwargs.update({"name":"help", "default":False, "prefix":"--", "implicit":True})
        super().__init__(**kwargs)

class VerboseParam(RepeatToggleParam): #[int]):
    """ The implicit -verbose flag """

    def __init__(self, **kwargs):
        kwargs.update({"name":"verbose", "default":0, "prefix":"-", "implicit":True})
        super().__init__(**kwargs)

class SeparatorParam(LiteralParam):
    """ A Parameter to separate subcmds """

    def __init__(self, **kwargs):
        kwargs.update({"name":"--", "prefix":"", "implicit":True})
        super().__init__(**kwargs)
