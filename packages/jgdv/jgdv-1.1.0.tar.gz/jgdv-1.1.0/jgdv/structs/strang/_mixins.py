#!/usr/bin/env python3
"""

"""
# mypy: disable-error-code="attr-defined,index,arg-type,call-arg"
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
import time
import types
import weakref
from uuid import UUID, uuid1

# ##-- end stdlib imports

from jgdv import Proto, Mixin
from jgdv.mixins.annotate import SubAnnotate_m
from ._interface import StrangMarker_e, GEN_K, INST_K

# ##-- types
# isort: off
import abc
import collections.abc
from typing import TYPE_CHECKING, cast, assert_type, assert_never
from typing import Generic, NewType
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

# isort: on
# ##-- end types

##-- logging
logging = logmod.getLogger(__name__)
logging.disabled = True
##-- end logging

class _Strang_cmp_m:
    """ The mixin of Strang Comparison methods """

    def __hash__(self) -> int:
        return str.__hash__(str(self))

    @override
    def __eq__(self, other:object) -> bool:
        match other:
            case _Strang_cmp_m():
                return hash(self) == hash(other)
            case str() if self._separator in other:
                return hash(self) == hash(other)
            case str():
                return hash(self[1:]) == hash(other)
            case _:
                return False

    def __lt__(self, other:str|Self) -> bool:
        match other:
            case _Strang_cmp_m() | str() if not len(self) < len(other):
                return False
            case _Strang_cmp_m():
                pass
            case _:
                raise NotImplementedError()

        if not self[0:] == other[0:]:
            return False

        for x,y in zip(self.body(), other.body(), strict=False):
            if x != y:
                return False

        return True

    def __le__(self, other:str) -> bool:
        return hash(self) == hash(other) or (self < other)

class _Strang_test_m:
    """ The mixin of strang test method """

    def is_uniq(self) -> bool:
        """ utility method to test if this name refers to a name with a UUID """
        return INST_K in self.metadata

    def is_head(self) -> bool:
        return self.bmark_e.head in self

    def __contains__(self, other:str) -> bool:
        """ test for conceptual containment of names
        other(a.b.c) ∈ self(a.b) ?
        ie: self < other
        """
        match other:
            case self.bmark_e() | UUID():
                return other in self._body_meta
            case self.gmark_e():
                return other in self._group_meta
            case str():
                return other in str(self)
            case _ if self.gmark_e is None:
                return False
            case _:
                return False

class _Strang_format_m:
    """ The mixin for formatting strangs into pure strings """

    def _format_subval(self, val:str, *, no_expansion:bool=False) -> str:
        match val:
            case str():
                return val
            case UUID() if no_expansion:
                return "<uuid>"
            case UUID():
                return f"<uuid:{val}>"
            case _:
                msg = "Unknown body type"
                raise TypeError(msg, val)

    def _expanded_str(self, *, stop:Maybe[int]=None) -> str:
        """ Create a str of the Strang with gen uuid's replaced with actual uuids """
        group = self[0:]
        body = []
        for val in self.body()[:stop]:
            match val:
                case str():
                    body.append(val)
                case UUID():
                    body.append(f"<uuid:{val}>")
                case _:
                    msg = "Unknown body type"
                    raise TypeError(msg, val)

        body_str = self._subjoin(body)
        return f"{group}{self._separator}{body_str}"

    def __format__(self, spec:str) -> str:
        """ format additions for strangs:
          {strang:g} = print only the group
          {strang:b} = print only the body

          """
        match spec:
            case "g":
                return self[0:]
            case "b":
                return self[1:]
            case _:
                return super().__format__(spec)

##--|

class _Strang_validation_m:
    """ The mixin for validating strangs on construction """

    @classmethod
    def pre_process(cls, data:str, *, strict:bool=False) -> str:  # noqa: ARG003
        """ run before str.__new__ is called, so can do early modification of the string
        Filters out extraneous duplicated separators
        """
        # TODO expand <uuid> gen tags here
        match data:
            case str() if 0 < str.count(data, cls._separator):
                subsep_double = re.escape(cls._subseparator * 2)
                clean_re      = re.compile(f"{subsep_double}+")
                cleaned       = clean_re.sub(cls._subseparator * 2, data)
                val           = cleaned.removesuffix(cls._subseparator).removesuffix(cls._subseparator)
                return val
            case _:
                msg = "Base data malformed"
                raise ValueError(msg, data)

    def _process(self) -> None:
        """ Get slices of the strang to describe group and body components """
        logging.debug("Processing Strang: %s", str.__str__(self))
        sep_index = self.find(self._separator)
        if sep_index == -1:
            msg = "Strang lacks a group{sep}body structure"
            raise ValueError(msg, str(self))

        self._group += self._get_slices(0, sep_index)
        self._body  += self._get_slices(sep_index, add_offset=True)
        if not (bool(self._group) and bool(self._body)):
            msg = "Strang doesn't have both a group and body"
            raise ValueError(msg)

        self._base_slices = (slice(self._group[0].start, self._group[-1].stop),
                             slice(self._body[0].start, self._body[-1].stop))

    def _get_slices(self, start:int=0, max:Maybe[int]=None, *, add_offset:bool=False) -> list[slice]:  # noqa: A002
        index, end, offset = start, max or len(self), len(self._subseparator)
        slices    = []
        if add_offset:
            index += len(self._separator)
        while -1 < index:
            match self.find(self._subseparator, index, end):
                case -1 if index == end:
                    index = -1
                case -1:
                    slices.append(slice(index, end))
                    index = -1
                case x:
                    slices.append(slice(index, x))
                    index = x + offset
        else:
            return slices

    def _post_process(self) -> None:
        """ Abstract no-op to do additional post-processing extraction of metadata """
        pass

class _Strang_subgen_m:
    """ Operations Mixin for manipulating TaskNames """

    @classmethod
    def _subjoin(cls, lst:list) -> str:
        return cls._subseparator.join(lst)

    def canon(self) -> Self:
        """ canonical name. no UUIDs
        eg: group::a.b.c.$gen$.<uuid>.c.d.e
        ->  group::a.b.c..c.d.e
        """
        group = self[0:]
        canon_body = self._subjoin(self.body(reject=lambda x: isinstance(x, UUID) or x == self.bmark_e.gen))

        return self.__class__(f"{group}{self._separator}{canon_body}")

    def pop(self, *, top:bool=False) -> Self:
        """
        Strip off one marker's worth of the name, or to the top marker.
        eg:
        root(test::a.b.c..<UUID>.sub..other) => test::a.b.c..<UUID>.sub
        root(test::a.b.c..<UUID>.sub..other, top=True) => test::a.b.c
        """
        end_id            = self._mark_idx[0 if top else 1]
        return self[2:end_id]

    def push(self, *vals:str) -> Self:
        """ Add a root marker if the last element isn't already a root marker
        eg: group::a.b.c => group.a.b.c.
        (note the trailing '.')
        """
        return self.__class__(self._subjoin(str(x) for x in [self[2:], self.bmark_e.mark, *vals] if x is not None))

    def to_uniq(self, *, suffix:Maybe[str]=None) -> Self:
        """ Generate a concrete instance of this name with a UUID appended,
        optionally can add a suffix

          ie: a.task.group::task.name..{prefix?}.$gen$.<UUID>
        """
        match self[1:-1]:
            case UUID():
                return self
            case _:
                return self.push(self.bmark_e.gen, "<uuid>", suffix)

    def de_uniq(self) -> Self:
        """ return the strang up to, but not including, the first instance mark.

        eg: 'group.a::q.w.e.<uuid>.t.<uuid>.y'.de_uniq() -> 'group.a::q.w.e'
        """
        if GEN_K not in self.metadata:
            return self
        return self[2:self.metadata.get(INST_K, None)].pop()

    def with_head(self) -> Self:
        """ generate a canonical group/completion task name for this name
        eg: (concrete) group::simple.task..$gen$.<UUID> ->  group::simple.task..$gen$.<UUID>..$group$
        eg: (abstract) group::simple.task. -> group::simple.task..$head$

        """
        if self.is_head():
            return self

        return self.push(self.bmark_e.head)

    def root(self) -> Self:
        """Pop off to the top marker """
        return self.pop(top=True)

##--|

class PostStrang_m(_Strang_validation_m,
                   _Strang_subgen_m,
                   SubAnnotate_m):
    """ Mixins that don't override str defaults """
    pass

class PreStrang_m(_Strang_cmp_m,
                  _Strang_test_m,
                  _Strang_format_m):
    """ Mixins that override str defaults """
    pass
