from uselessutilities import *

def test_addition():
    assert ter(10) + ter(10) == ter(20)
    assert quat(10) + quat(10) == quat(20)
    assert quin(10) + quin(10) == quin(20)
    assert sen(10) + sen(10) == sen(20)
    assert sept(10) + sept(10) == sept(20)

    assert ter(10) + quat(10) == ter(20)
    assert ter(10) + quin(10) == ter(20)
    assert ter(10) + sen(10) == ter(20)
    assert ter(10) + sept(10) == ter(20)

    assert quat(10) + ter(10) == quat(20)
    assert quat(10) + quin(10) == quat(20)
    assert quat(10) + sen(10) == quat(20)
    assert quat(10) + sept(10) == quat(20)

    assert quin(10) + ter(10) == quin(20)
    assert quin(10) + quat(10) == quin(20)
    assert quin(10) + sen(10) == quin(20)
    assert quin(10) + sept(10) == quin(20)

    assert sen(10) + ter(10) == sen(20)
    assert sen(10) + quat(10) == sen(20)
    assert sen(10) + quin(10) == sen(20)
    assert sen(10) + sept(10) == sen(20)

    assert sept(10) + ter(10) == sept(20)
    assert sept(10) + quat(10) == sept(20)
    assert sept(10) + quin(10) == sept(20)
    assert sept(10) + sen(10) == sept(20)

    assert ter(10) + 10 == ter(20)
    assert quat(10) + 10 == quat(20)
    assert quin(10) + 10 == quin(20)
    assert sen(10) + 10 == sen(20)
    assert sept(10) + 10 == sept(20)

def test_subtraction():
    assert ter(10) - ter(10) == ter(0)
    assert quat(10) - quat(10) == quat(0)
    assert quin(10) - quin(10) == quin(0)
    assert sen(10) - sen(10) == sen(0)
    assert sept(10) - sept(10) == sept(0)

    assert ter(10) - quat(10) == ter(0)
    assert ter(10) - quin(10) == ter(0)
    assert ter(10) - sen(10) == ter(0)
    assert ter(10) - sept(10) == ter(0)

    assert quat(10) - ter(10) == quat(0)
    assert quat(10) - quin(10) == quat(0)
    assert quat(10) - sen(10) == quat(0)
    assert quat(10) - sept(10) == quat(0)

    assert quin(10) - ter(10) == quin(0)
    assert quin(10) - quat(10) == quin(0)
    assert quin(10) - sen(10) == quin(0)
    assert quin(10) - sept(10) == quin(0)

    assert sen(10) - ter(10) == sen(0)
    assert sen(10) - quat(10) == sen(0)
    assert sen(10) - quin(10) == sen(0)
    assert sen(10) - sept(10) == sen(0)

    assert sept(10) - ter(10) == sept(0)
    assert sept(10) - quat(10) == sept(0)
    assert sept(10) - quin(10) == sept(0)
    assert sept(10) - sen(10) == sept(0)

    assert sen(10) - 10 == sen(0)
    assert quat(10) - 10 == quat(0)
    assert quin(10) - 10 == quin(0)
    assert sen(10) - 10 == sen(0)
    assert sept(10) - 10 == sept(0)

def test_multiplication():
    assert ter(10) * ter(10) == ter(100)
    assert quat(10) * quat(10) == quat(100)
    assert quin(10) * quin(10) == quin(100)
    assert sen(10) * sen(10) == sen(100)
    assert sept(10) * sept(10) == sept(100)

    assert ter(10) * quat(10) == ter(100)
    assert ter(10) * quin(10) == ter(100)
    assert ter(10) * sen(10) == ter(100)
    assert ter(10) * sept(10) == ter(100)

    assert quat(10) * ter(10) == quat(100)
    assert quat(10) * quin(10) == quat(100)
    assert quat(10) * sen(10) == quat(100)
    assert quat(10) * sept(10) == quat(100)

    assert quin(10) * ter(10) == quin(100)
    assert quin(10) * quat(10) == quin(100)
    assert quin(10) * sen(10) == quin(100)
    assert quin(10) * sept(10) == quin(100)

    assert sen(10) * ter(10) == sen(100)
    assert sen(10) * quat(10) == sen(100)
    assert sen(10) * quin(10) == sen(100)
    assert sen(10) * sept(10) == sen(100)

    assert sept(10) * ter(10) == sept(100)
    assert sept(10) * quat(10) == sept(100)
    assert sept(10) * quin(10) == sept(100)
    assert sept(10) * sen(10) == sept(100)

    assert ter(10) * 10 == ter(100)
    assert quat(10) * 10 == quat(100)
    assert quin(10) * 10 == quin(100)
    assert sen(10) * 10 == sen(100)
    assert sept(10) * 10 == sept(100)

def test_division():
    assert ter(10) / ter(10) == ter(1)
    assert quat(10) / quat(10) == quat(1)
    assert quin(10) / quin(10) == quin(1)
    assert sen(10) / sen(10) == sen(1)
    assert sept(10) / sept(10) == sept(1)

    assert ter(10) / quat(10) == ter(1)
    assert ter(10) / quin(10) == ter(1)
    assert ter(10) / sen(10) == ter(1)
    assert ter(10) / sept(10) == ter(1)

    assert quat(10) / ter(10) == quat(1)
    assert quat(10) / quin(10) == quat(1)
    assert quat(10) / sen(10) == quat(1)
    assert quat(10) / sept(10) == quat(1)

    assert quin(10) / ter(10) == quin(1)
    assert quin(10) / quat(10) == quin(1)
    assert quin(10) / sen(10) == quin(1)
    assert quin(10) / sept(10) == quin(1)

    assert sen(10) / ter(10) == sen(1)
    assert sen(10) / quat(10) == sen(1)
    assert sen(10) / quin(10) == sen(1)
    assert sen(10) / sept(10) == sen(1)

    assert sept(10) / ter(10) == sept(1)
    assert sept(10) / quat(10) == sept(1)
    assert sept(10) / quin(10) == sept(1)
    assert sept(10) / sen(10) == sept(1)

    assert ter(10) / 10 == ter(1)
    assert quat(10) / 10 == quat(1)
    assert quin(10) / 10 == quin(1)
    assert sen(10) / 10 == sen(1)
    assert sept(10) / 10 == sept(1)

def test_modulo():
    assert ter(10) % ter(10) == ter(0)
    assert quat(10) % quat(10) == quat(0)
    assert quin(10) % quin(10) == quin(0)
    assert sen(10) % sen(10) == sen(0)
    assert sept(10) % sept(10) == sept(0)

    assert ter(10) % quat(10) == ter(0)
    assert ter(10) % quin(10) == ter(0)
    assert ter(10) % sen(10) == ter(0)
    assert ter(10) % sept(10) == ter(0)

    assert quat(10) % ter(10) == quat(0)
    assert quat(10) % quin(10) == quat(0)
    assert quat(10) % sen(10) == quat(0)
    assert quat(10) % sept(10) == quat(0)

    assert quin(10) % ter(10) == quin(0)
    assert quin(10) % quat(10) == quin(0)
    assert quin(10) % sen(10) == quin(0)
    assert quin(10) % sept(10) == quin(0)

    assert sen(10) % ter(10) == sen(0)
    assert sen(10) % quat(10) == sen(0)
    assert sen(10) % quin(10) == sen(0)
    assert sen(10) % sept(10) == sen(0)

    assert sept(10) % ter(10) == sept(0)
    assert sept(10) % quat(10) == sept(0)
    assert sept(10) % quin(10) == sept(0)
    assert sept(10) % sen(10) == sept(0)

    assert ter(10) % 10 == ter(0)
    assert quat(10) % 10 == quat(0)
    assert quin(10) % 10 == quin(0)
    assert sen(10) % 10 == sen(0)
    assert sept(10) % 10 == sept(0)