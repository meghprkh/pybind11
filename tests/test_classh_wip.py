# -*- coding: utf-8 -*-
import pytest

from pybind11_tests import classh_wip as m


def test_mpty_constructors():
    e = m.mpty()
    assert e.__class__.__name__ == "mpty"
    e = m.mpty("")
    assert e.__class__.__name__ == "mpty"
    e = m.mpty("txtm")
    assert e.__class__.__name__ == "mpty"


def test_cast():
    assert m.get_mtxt(m.rtrn_mpty_valu()) == "rtrn_valu"
    assert m.get_mtxt(m.rtrn_mpty_rref()) == "rtrn_rref"
    assert m.get_mtxt(m.rtrn_mpty_cref()) == "rtrn_cref"
    assert m.get_mtxt(m.rtrn_mpty_mref()) == "rtrn_mref"
    assert m.get_mtxt(m.rtrn_mpty_cptr()) == "rtrn_cptr"
    assert m.get_mtxt(m.rtrn_mpty_mptr()) == "rtrn_mptr"


def test_load():
    assert m.pass_mpty_valu(m.mpty("Valu")) == "pass_valu:Valu"
    assert m.pass_mpty_rref(m.mpty("Rref")) == "pass_rref:Rref"
    assert m.pass_mpty_cref(m.mpty("Cref")) == "pass_cref:Cref"
    assert m.pass_mpty_mref(m.mpty("Mref")) == "pass_mref:Mref"
    assert m.pass_mpty_cptr(m.mpty("Cptr")) == "pass_cptr:Cptr"
    assert m.pass_mpty_mptr(m.mpty("Mptr")) == "pass_mptr:Mptr"


def test_cast_shared_ptr():
    assert m.get_mtxt(m.rtrn_mpty_shmp()) == "rtrn_shmp"
    assert m.get_mtxt(m.rtrn_mpty_shcp()) == "rtrn_shcp"


def test_load_shared_ptr():
    assert m.pass_mpty_shmp(m.mpty("Shmp")) == "pass_shmp:Shmp"
    assert m.pass_mpty_shcp(m.mpty("Shcp")) == "pass_shcp:Shcp"


def test_cast_unique_ptr():
    assert m.get_mtxt(m.rtrn_mpty_uqmp()) == "rtrn_uqmp"
    assert m.get_mtxt(m.rtrn_mpty_uqcp()) == "rtrn_uqcp"


def test_load_unique_ptr():
    assert m.pass_mpty_uqmp(m.mpty("Uqmp")) == "pass_uqmp:Uqmp"
    assert m.pass_mpty_uqcp(m.mpty("Uqcp")) == "pass_uqcp:Uqcp"


@pytest.mark.parametrize(
    "pass_mpty, argm, rtrn",
    [
        (m.pass_mpty_uqmp, "Uqmp", "pass_uqmp:Uqmp"),
        (m.pass_mpty_uqcp, "Uqcp", "pass_uqcp:Uqcp"),
    ],
)
def test_pass_unique_ptr_disowns(pass_mpty, argm, rtrn):
    obj = m.mpty(argm)
    assert pass_mpty(obj) == rtrn
    with pytest.raises(RuntimeError) as exc_info:
        m.pass_mpty_uqmp(obj)
    assert str(exc_info.value) == (
        "Missing value for wrapped C++ type:"
        " Python instance is uninitialized or was disowned."
    )


def test_unique_ptr_roundtrip(num_round_trips=1000):
    # Multiple roundtrips to stress-test instance registration/deregistration.
    recycled = m.mpty("passenger")
    for _ in range(num_round_trips):
        id_orig = id(recycled)
        recycled = m.unique_ptr_roundtrip(recycled)
        assert m.get_mtxt(recycled) == "passenger"
        id_rtrn = id(recycled)
        # Ensure the returned object is a different Python instance.
        assert id_rtrn != id_orig
        id_orig = id_rtrn
