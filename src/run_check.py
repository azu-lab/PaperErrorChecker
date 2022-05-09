import argparse
import glob
import os
import re
from logging import INFO, Formatter, StreamHandler, getLogger
from typing import Dict, List

import yaml

# Logger setting
handler = StreamHandler()
handler.setLevel(INFO)
fmt = '[%(levelname)s] %(message)s'
formatter = Formatter(fmt)
handler.setFormatter(formatter)
logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(handler)


def option_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-d",
        "--check_dir",
        required=True,
        type=str,
        help="Path to directory containing tex files to be checked"
    )
    args = arg_parser.parse_args()

    return args.check_dir


class Checker():
    def __init__(
        self,
        file_paths: List[str]
    ) -> None:
        self._target_paths = {"all": file_paths}
        intro_path = [p for p in file_paths
                      if "Introduction" in p][0]
        self._target_paths["introduction"] = intro_path
        self._target_paths["except for main"] = [p for p in file_paths
                                                 if 'Main' not in p]

    def check(
        self,
        pattern: str,
        check_type: str,
        target: str,
        flags=None,
    ) -> List[str]:
        if(check_type == "line"):
            return self._check_per_line(pattern, flags, target)

    def _check_per_line(
        self,
        pattern: str,
        flags,
        target: str
    ) -> List[str]:
        errors = []
        for tex_path in self._target_paths[target]:
            with open(tex_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            for line_count, line in enumerate(lines):
                if(flags):
                    result = re.findall(pattern, line, flags)
                else:
                    result = re.findall(pattern, line)
                if(result):
                    for match in result:
                        errors.append(' | '.join([
                            os.path.basename(tex_path),
                            str(line_count+1),
                            match])
                        )

        return errors


def print_log(
    msg: str,
    level: str,
    errors: List[str]


) -> None:
    if(errors):
        if(level == 'info'):
            logger.info(msg)
        elif(level == 'warning'):
            logger.warning(msg)
        elif(level == 'error'):
            logger.error(msg)
        else:
            raise NotImplementedError

        [print(f"\t{error}") for error in errors]
        print("------------------------------------------------------------")


def get_check_args(args_dict: Dict) -> Dict:
    args = {"pattern": args_dict['pattern']}
    flags_str = args_dict.get("flags")
    if(flags_str == "ignorecase"):
        args['flags'] = re.IGNORECASE

    args["target"] = args_dict.get("target", "all")
    args["check_type"] = args_dict.get("check type", "line")

    return args


def main(check_dir):
    tex_paths = glob.glob(f"{check_dir}/**/*.tex",
                          recursive=True)
    checker = Checker(tex_paths)

    # Load check list
    with open(
        f"{os.path.dirname(__file__)}/check_lists/check_list.yaml",
        'r'
    ) as f:
        check_list = yaml.safe_load(f)

    # Check
    for msg, args_dict in check_list.items():
        check_args = get_check_args(args_dict)
        errors = checker.check(**check_args)
        print_log(msg, args_dict['level'], errors)


if __name__ == "__main__":
    check_dir = option_parser()
    main(check_dir)
