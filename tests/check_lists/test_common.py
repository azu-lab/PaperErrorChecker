import os

from src.run_checker import Checker
from tests.check_lists.conftest import get_one_check_dict


def test_cite(mocker, capfd):
    mocker.patch("src.run_checker.Checker._get_check_lists",
                 return_value=get_one_check_dict(
                     "common", r"\cite{X}, \cite{Y} -> \cite{X, Y}"))
    Checker(f"{os.path.dirname(__file__)}/test_common", "")
    out, err = capfd.readouterr()
