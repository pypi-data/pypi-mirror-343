from uselessutilities import ter, quat, quin, sen, sept, non

def test_ter_basic():
    t = ter(10)
    assert str(t) == "0t101"
    assert int(t) == 10
    assert float(t) == 10.0

def test_quat_basic():
    q = quat(10)
    assert str(q) == "0q22"
    assert int(q) == 10
    assert float(q) == 10.0

def test_quin_basic():
    Q = quin(10)
    assert str(Q) == "0Q20"
    assert int(Q) == 10
    assert float(Q) == 10.0

def test_sen_basic():
    s = sen(10)
    assert str(s) == "0s14"
    assert int(s) == 10
    assert float(s) == 10.0

def test_sept_basic():
    S = sept(10)
    assert str(S) == "0S13"
    assert int(S) == 10
    assert float(S) == 10.0

def test_non_basic():
    n = non(10)
    assert str(n) == "0n11"
    assert int(n) == 10
    assert float(n) == 10.0