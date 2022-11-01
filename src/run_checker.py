import argparse
import glob
import os
import re
from logging import INFO, Formatter, StreamHandler, getLogger
from typing import Any, Dict, List, Tuple

import yaml

# Logger setting
handler = StreamHandler()
handler.setLevel(INFO)
fmt = '%(levelname)-8s: %(asctime)s | %(message)s'
formatter = Formatter(
    fmt,
    datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(handler)


class Checker:
    def __init__(
        self,
        check_dir: str,
        format: str
    ) -> None:
        self._tex_path_dict = Checker._get_tex_path_dict(check_dir)
        self._check_lists = Checker._get_check_lists(format)

    def check(self) -> None:
        for msg, options in self._check_lists.items():
            pattern, level, target, flags = Checker._perse_options(options)
            errors = []
            for tex_path in self._tex_path_dict[target]:
                with open(tex_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line_count, line in enumerate(lines):
                    if Checker._is_skip_line(line):
                        continue
                    if flags:
                        matches = re.finditer(pattern, line, flags)
                    else:
                        matches = re.finditer(pattern, line)
                    if matches:
                        for match in matches:
                            red_marked_line = (
                                line[:match.start()] + "\033[91m"
                                + line[match.start():match.end()]
                                + "\033[0m" + line[match.end():]
                            )
                            errors.append(" | ".join([
                                os.path.basename(tex_path),
                                str(line_count+1),
                                red_marked_line
                            ]))

            Checker._print_log(msg, level, errors)

    @staticmethod
    def _is_skip_line(line: str) -> bool:
        line = line.replace(' ', '')

        skip_heads = [
            r'\usepackage',
            r'\graphicspath',
            r'\hypersetup',
            r'\urlstyle',
            r'\title',
            r'\author',
            r'\documentclass',
            r'\theoremstyle',
            r'\newtheorem',
            r'\algdef',
            r'\algnewcommand',
            r'\setcounter',
            r'\renewcommand',
            r'\newcommand',
            r'\def',
            r'\history',
            r'\doi',
            r'\corresp',
            r'\input',
            r'\label',
            r'\bibliography',
            r'%'
        ]
        for skip_head in skip_heads:
            if line.startswith(skip_head):
                return True

        return False

    @staticmethod
    def _print_log(
        msg: str,
        level: str,
        errors: List[str]
    ) -> None:
        if errors:
            if level == "info":
                print(f'[INFO] {msg}')
            elif level == "warning":
                print(f'[WARNING] {msg}')
            elif level == "error":
                print(f'[ERROR] {msg}')
            else:
                raise NotImplementedError

            for error in errors:
                print(f"\t{error}")
            print("----------------------------------------------------------")

    @staticmethod
    def _perse_options(
        options: Dict
    ) -> Tuple[str, str, str, Any]:
        level = options.get("level")
        if not level or level.lower() not in ["error", "warning", "info"]:
            logger.error('Specify "error", "warning", or "info" for "level".')
            exit(1)

        target = options.get("target", "all")
        if (target.lower() not in ["all",
                                   "introduction",
                                   "abstract",
                                   "except for abstract"]):
            logger.error('Specify "all", "introduction", "abstract", '
                         'or "except for abstract" for "target".')
            exit(1)

        flags = options.get("flags")
        if flags:
            if flags.lower() == "ignorecase":
                flags = re.IGNORECASE
            else:
                logger.error('Specify "ignorecase" for "flags".')
                exit(1)

        return options["pattern"], level, target, flags

    @staticmethod
    def _get_check_lists(
        format: str
    ) -> Dict:
        with open(
            f"{os.path.dirname(__file__)}/check_lists/common.yaml",
            "r"
        ) as f:
            check_lists = yaml.safe_load(f)

        with open(
            f"{os.path.dirname(__file__)}/check_lists/{format}.yaml",
            "r"
        ) as f:
            check_lists.update(yaml.safe_load(f))

        return check_lists

    @staticmethod
    def _get_tex_path_dict(
        check_dir: str
    ) -> Dict:
        tex_paths = glob.glob(f"{check_dir}/**/*.tex",
                              recursive=True)
        target_path_dict = {"all": tex_paths}
        target_path_dict["introduction"] = [p for p in tex_paths
                                            if "intro" in p.lower()]
        target_path_dict["abstract"] = [p for p in tex_paths
                                        if "abst" in p.lower()]
        target_path_dict["except for abstract"] = [p for p in tex_paths
                                                   if "abst" not in p.lower()]

        return target_path_dict


def option_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-d",
        "--check_dir",
        required=True,
        type=str,
        help="Path to directory containing tex files to be checked"
    )
    arg_parser.add_argument(
        "-f",
        "--format",
        required=False,
        type=str,
        default="conference",
        help="Where to submit your paper"
    )
    args = arg_parser.parse_args()

    return args.check_dir, args.format


if __name__ == "__main__":
    check_dir, format = option_parser()
    if not os.path.exists(check_dir):
        logger.error('Directory not found.')
        exit(1)
    checker = Checker(check_dir, format)
    checker.check()
