#!/usr/bin/env python3
"""

"""
from __future__ import annotations

import logging as logmod
import pathlib as pl
from typing import (Any, Callable, ClassVar, Generic, Iterable, Iterator,
                    Mapping, Match, MutableMapping, Sequence, Tuple, TypeAlias,
                    TypeVar, cast)
from types import MethodType
import warnings

import pytest

from jgdv import JGDVError
from jgdv.structs.dkey import DKey, DKeyed
from jgdv.structs.dkey import DKeyExpansionDecorator as DKexd
from jgdv.decorators import DForm_e
from jgdv.structs.dkey.decorator import DKeyMetaDecorator, DKeyedMeta, DKeyedRetrieval

logging = logmod.root

class TestDkeyDecorator:

    def test_sanity(self):
        assert(True is not False)

    def test_initial(self):
        value = DKexd([])
        assert(isinstance(value, DKexd))

    def test_with_key(self):
        value = DKexd([DKey("test")])
        assert(isinstance(value, DKexd))
        assert(bool(value._data))

    def test_validate_sig_method_head(self):
        dec   = DKexd([])
        ttype = DForm_e.METHOD

        def simple(self, spec, state):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [])
        assert(True)

    def test_validate_sig_method_head_fail(self):
        dec   = DKexd([])
        ttype = DForm_e.METHOD

        def simple(self, spec, notstate):
            pass

        sig = dec._signature(simple)
        with pytest.raises(JGDVError):
            dec._validate_sig_h(sig, ttype, [])

    def test_validate_sig_func_head(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, state):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [])
        assert(True)

    def test_validate_sig_func_head_fail(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, notstate):
            pass

        sig = dec._signature(simple)
        with pytest.raises(JGDVError):
            dec._validate_sig_h(sig, ttype, [])

    def test_validate_sig_method_tail(self):
        dec   = DKexd([])
        ttype = DForm_e.METHOD

        def simple(self, spec, state, bloo, blee):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [DKey("bloo"), DKey("blee")])
        assert(True)

    def test_validate_sig_method_tail_fail(self):
        dec   = DKexd([])
        ttype = DForm_e.METHOD

        def simple(self, spec, state, bloo, blee):
            pass

        sig = dec._signature(simple)
        with pytest.raises(JGDVError):
            dec._validate_sig_h(sig, ttype, [DKey("bloo"), DKey("blah")])

    def test_validate_sig_func_tail(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, state, bloo, blee):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [DKey("bloo"), DKey("blee")])
        assert(True)

    def test_validate_sig_func_tail_fail(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, state, bloo, blee):
            pass

        sig = dec._signature(simple)
        with pytest.raises(JGDVError):
            dec._validate_sig_h(sig, ttype, [DKey("bloo"), DKey("blah")])

    def test_validate_sig_incomplete_tail(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, state, bloo, blee, blob):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [DKey("blee"), DKey("blob")])
        assert(True)

    def test_validate_sig_skip_ignores(self):
        dec   = DKexd([])
        ttype = DForm_e.FUNC

        def simple(spec, state, _bloo, blee_ex, blob):
            pass

        sig = dec._signature(simple)
        dec._validate_sig_h(sig, ttype, [DKey("awef"), DKey("aweg"), DKey("blob")])
        assert(True)

class TestDKeyDecoratorExpansion:

    def test_sanity(self):
        assert(True is not False)

    def test_basic(self):
        state = { "basic": "blah" }

        @DKeyed.types("basic")
        def simple(spec, state, basic):
            assert(basic == "blah")

        simple(None, state)

    def test_mismatch_signature(self):
        with pytest.raises(JGDVError):
            @DKeyed.types("other")
            def simple(spec, state, basic):
                assert(basic == "blah")

    def test_expansion_fallback(self):
        state = { "notbasic": "bloo" }

        @DKeyed.types("basic", fallback="blah")
        def simple(spec, state, basic):
            assert(basic == "blah")

        simple(None, state)

    def test_multi_expansion(self):
        state = { "basic": "bloo", "other": "qwerty" }

        @DKeyed.types("basic", fallback="blah")
        @DKeyed.types("other", fallback="aweg")
        def simple(spec, state, basic, other):
            assert(basic == "bloo")
            assert(other == "qwerty")

        simple(None, state)

    def test_multi_expansion_fallback(self):
        state = { "notbasic": "bloo", "notother": "qwerty" }

        @DKeyed.types("basic", fallback="blah")
        @DKeyed.types("other", fallback="aweg")
        def simple(spec, state, basic, other):
            assert(basic == "blah")
            assert(other == "aweg")

        simple(None, state)

    def test_meta_decorator_no_change(self):

        @DKeyed.requires("basic")
        @DKeyed.requires("other")
        def simple(spec, state):
            pass

        simple(None, None)


    def test_redirects_expansion(self):

        @DKeyed.redirects("other_")
        def simple(spec, state, _other):
            match _other:
                case str():
                    assert(_other == "blah")
                case x:
                    assert(False), x

        simple(None, {"other_":"blah"})


    def test_redirects_expansion_doesnt_recurse(self):

        @DKeyed.redirects("other_")
        def simple(spec, state, _other):
            match _other:
                case DKey():
                    assert(_other == "blah")
                case x:
                    assert(False), x

        simple(None, {"other_":"blah", "blah":"bloo"})

class TestDKeyed:

    def test_sanity(self):
        assert(True is not False) # noqa: PLR0133

    def test_basic(self):
        assert(DKeyedMeta in DKeyed._extensions)
        assert(DKeyedRetrieval in DKeyed._extensions)

    def test_simple_access(self):
        assert(hasattr(DKeyedMeta, "requires"))
        assert(hasattr(DKeyed, "requires"))
        match DKeyed.requires:
            case MethodType():
                assert(True)
            case x:
                assert(False), x


    @pytest.mark.skip
    def test_todo(self):
        pass
