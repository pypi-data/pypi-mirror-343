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
import time
import types
import weakref
from typing import (TYPE_CHECKING, Any, Callable, ClassVar, Final, Generator,
                    Generic, Iterable, Iterator, Mapping, Match,
                    MutableMapping, Protocol, Sequence, Tuple, TypeAlias,
                    TypeGuard, TypeVar, cast, final, overload,
                    runtime_checkable)
from uuid import UUID, uuid1

# ##-- end stdlib imports

# ##-- 1st party imports
from jgdv import Maybe
from jgdv.enums import LoopControl_e
from jgdv.structs.dkey import DKey
# ##-- end 1st party imports

##-- logging
logging = logmod.getLogger(__name__)
##-- end logging

MARKER       : Final[str]  = ".marker"
walk_ignores : Final[list] = ['.git', '.DS_Store', "__pycache__"] # TODO use a .ignore file
walk_halts   : Final[str]  = [".doot_ignore"]

class PathManip_m:
    """
      A Mixin for common path manipulations
    """

    def _calc_path_parts(self, fpath:pl.Path, roots:list[pl.Path]) -> dict:
        """ take a path, and get a dict of bits which aren't methods of Path
          if no roots are provided use cwd
        """
        assert(fpath is not None)
        assert(isinstance(roots, list))

        temp_stem  = fpath
        # This handles "a/b/c.tar.gz"
        while temp_stem.stem != temp_stem.with_suffix("").stem:
            temp_stem = temp_stem.with_suffix("")

        return {
            'rpath'   : self._get_relative(fpath, roots),
            'fstem'   : temp_stem.stem,
            'fparent' : fpath.parent,
            'fname'   : fpath.name,
            'fext'    : fpath.suffix,
            'pstem'   : fpath.parent.stem,
            }

    def _build_roots(self, spec, state, roots:Maybe[list[str|DKey]]) -> list[pl.Path]:
        """
        convert roots from keys to paths
        """
        roots   = roots or []
        results = []
        for root in roots:
            root_key = DKey(root, fallback=root, mark=DKey.Mark.PATH)
            results.append(root_key.expand(spec, state))
        else:
            return results

    def _get_relative(self, fpath, roots:Maybe[list[pl.Path]]=None) -> pl.Path:
        """ Get relative path of fpath.
          if no roots are provided, default to using cwd
        """
        logging.debug("Finding Relative Path of: %s using %s", fpath, roots)
        if not fpath.is_absolute():
            return fpath

        roots = roots or [pl.Path.cwd()]

        for root_path in roots:
            try:
                return fpath.relative_to(root_path)
            except ValueError:
                continue

        raise ValueError(f"{fpath} is not able to be made relative", roots)

    def _shadow_path(self, rpath:pl.Path, shadow_root:pl.Path) -> pl.Path:
        """ take a relative path, apply it onto a root to create a shadowed location """
        raise NotImplementedError()

    def _find_parent_marker(self, fpath, marker=None) -> Maybe[pl.Path]:
        """ Go up the parent list to find a marker file, return the dir its in """
        marker = marker or MARKER
        for p in fpath.parents:
            if (p / marker).exists():
                return p

        return None

    def _normalize(self, path:pl.Path, root=None, symlinks:bool=False) -> pl.Path:
        """
          a basic path normalization
          expands user, and resolves the location to be absolute
        """
        result = path
        if symlinks and path.is_symlink():
            raise NotImplementedError("symlink normalization", path)

        match result.parts:
            case ["~", *_]:
                result = result.expanduser().resolve()
            case ["/", *_]:
                result = result
            case _ if root:
                result = (root / path).expanduser().resolve()
            case _:
                pass

        return result

class Walker_m:
    """ A Mixin for walking directories,
      written for py<3.12
      """
    control_e = LoopControl_e

    def walk_all(self, roots, exts, rec=False, fn=None) -> Generator[dict]:
        """
        walk all available targets,
        and generate unique names for them
        """
        result = []
        match rec:
            case True:
                for root in roots:
                    result += self.walk_target_deep(root, exts, fn)
            case False:
                for root in roots:
                    result += self.walk_target_shallow(root, exts, fn)

        return result

    def walk_target_deep(self, target, exts, fn) -> Generator[pl.Path]:
        logging.info("Deep Walking Target: %s : exts=%s", target, exts)
        if not target.exists():
            return None

        queue = [target]
        while bool(queue):
            current = queue.pop()
            if not current.exists():
                continue
            if current.name in walk_ignores:
                continue
            if current.is_dir() and any([(current / x).exists() for x in walk_halts]):
                continue
            if bool(exts) and current.is_file() and current.suffix not in exts:
                continue
            match fn(current):
                case self.control_e.yes:
                    yield current
                case True if current.is_dir():
                    queue += sorted(current.iterdir())
                case True | self.control_e.yesAnd:
                    yield current
                    if current.is_dir():
                        queue += sorted(current.iterdir())
                case False | self.control_e.noBut if current.is_dir():
                    queue += sorted(current.iterdir())
                case None | False:
                    continue
                case self.control_e.no | self.control_e.noBut:
                    continue
                case _ as x:
                    raise TypeError("Unexpected filter value", x)

    def walk_target_shallow(self, target, exts, fn):
        logging.debug("Shallow Walking Target: %s", target)
        if target.is_file():
            fn_fail = fn(target) in [None, False, self.control_e.no, self.control_e.noBut]
            ignore  = target.name in walk_ignores
            bad_ext = (bool(exts) and target.suffix in exts)
            if not (fn_fail or ignore or bad_ext):
                yield target
            return None

        for x in target.iterdir():
            fn_fail = fn(x) in [None, False, self.control_e.no, self.control_e.noBut]
            ignore  = x.name in walk_ignores
            bad_ext = bool(exts) and x.is_file() and x.suffix not in exts
            if not (fn_fail or ignore or bad_ext):
                yield x
