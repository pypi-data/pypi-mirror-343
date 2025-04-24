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

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType, Any, Callable
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

class AssignParam(ParamSpecBase):
    """ TODO a joined --key=val param """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("prefix", "--")
        kwargs.setdefault("separator", "=")
        kwargs.setdefault("type", str)
        super().__init__(*args, **kwargs)

    def next_value(self, args:list) -> tuple[str, list, int]:
        """ get the value for a --key=val """
        logging.debug("Getting Key Assignment: %s : %s", self.name, args)
        if self.separator not in args[0]:
            raise ArgParseError("Assignment param has no assignment", self.separator, args[0])
        key,val = self._split_assignment(args[0])
        return self.name, [val], 1

class WildcardParam(AssignParam):
    """ TODO a wildcard param that matches any --{key}={val} """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("type", str)
        kwargs['name'] = "*"
        super().__init__(**kwargs)

    def matches_head(self, val) -> bool:
        return (val.startswith(self.prefix)
                and self.separator in val)

    def next_value(self, args:list) -> tuple[str, list, int]:
        logging.debug("Getting Wildcard Key Assingment: %s", args)
        assert(self.separator in args[0]), (self.separator, args[0])
        key,val = self._split_assignment(args[0])
        return key.removeprefix(self.prefix), [val], 1

