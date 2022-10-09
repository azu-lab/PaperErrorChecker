import os

from src.run_checker import Checker
from tests.check_lists.conftest import get_one_check_dict


def test_cite(mocker, capfd):
    mocker.patch("src.run_checker.Checker._get_check_lists",
                 return_value=get_one_check_dict(
                     "common", r"\cite{X}, \cite{Y} -> \cite{X, Y}"))
    checker = Checker(f"{os.path.dirname(__file__)}/test_common", "")
    checker.check()
    out, err = capfd.readouterr()
    assert "| 1 |" in out
    assert "| 2 |" in out
    assert "| 3 |" in out
    assert "| 4 |" in out


def test_insert_a_period(mocker, capfd):
    mocker.patch("src.run_checker.Checker._get_check_lists",
                 return_value=get_one_check_dict(
                     "common", r"Insert a period"))
    checker = Checker(f"{os.path.dirname(__file__)}/test_common", "")
    checker.check()
    out, err = capfd.readouterr()
    assert "| 7 |" not in out
    assert "| 8 |" in out
    assert "| 9 |" in out
    assert "| 10 |" not in out
    assert "| 11 |" in out
    assert "| 12 |" in out
    assert "| 13 |" in out
    assert "| 14 |" in out
    assert "| 15 |" not in out
    assert "| 16 |" in out
    assert "| 17 |" in out
