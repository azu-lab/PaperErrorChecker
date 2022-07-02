import os
from typing import Dict

import yaml


def get_one_check_dict(
    format: str,
    msg: str
) -> Dict:
    if format == "common":
        with open(
            f"{os.path.dirname(__file__)}/../../src/check_lists/common.yaml",
            "r"
        ) as f:
            check_lists = yaml.safe_load(f)
    elif format == "conference":
        with open(
            f"{os.path.dirname(__file__)}/../../src/check_lists/conference.yaml",
            "r"
        ) as f:
            check_lists = yaml.safe_load(f)
    elif format == "thesis":
        with open(
            f"{os.path.dirname(__file__)}/../../src/check_lists/thesis.yaml",
            "r"
        ) as f:
            check_lists = yaml.safe_load(f)

    return {msg: check_lists[msg]}
