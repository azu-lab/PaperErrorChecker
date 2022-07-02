import argparse
import glob
import os
import re
from logging import getLogger
from typing import Any, Dict, List, Tuple

import yaml

logger = getLogger(__name__)


class Checker:
    def __init__(
        self,
        check_dir: str,
        format: str
    ) -> None:
        target_path_dict = Checker._get_target_path_dict(check_dir)
        check_lists = Checker._get_check_lists(format)

        for msg, options in check_lists.items():
            pattern, level, target, flags = Checker._perse_options(options)
            errors = []
            for tex_path in target_path_dict[target]:
                with open(tex_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line_count, line in enumerate(lines):
                    if flags:
                        matches = re.finditer(pattern, line, flags)
                    else:
                        matches = re.finditer(pattern, line)
                    if matches:
                        for match in matches:
                            head = line[:match.start()]
                            tail = line[match.end():]
                            match_str = line[match.start():match.end()]
                            out = (head + "\033[91m"
                                   + match_str + "\033[0m" + tail)

                            errors.append(" | ".join([
                                os.path.basename(tex_path),
                                str(line_count+1),
                                out])
                            )

            Checker._print_log(msg, level, errors)

    @staticmethod
    def _print_log(
        msg: str,
        level: str,
        errors: List[str]
    ) -> None:
        if errors:
            if level == "info":
                logger.info(msg)
            elif level == "warning":
                logger.warning(msg)
            elif level == "error":
                logger.error(msg)
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
    def _get_target_path_dict(
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
    Checker(check_dir, format)
