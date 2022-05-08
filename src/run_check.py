import argparse
import glob
import os
import pprint
import re
from logging import ERROR, INFO, WARNING, Formatter, StreamHandler, getLogger
from typing import List, Tuple, Union

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


class CheckerPerLine():
    def __init__(
        self,
        file_paths: List[str]
    ) -> None:
        self._file_paths = file_paths

    def check(
        self,
        pattern: str,
        flags=None
    ) -> List[str]:
        errors = []
        for tex_path in self._file_paths:
            with open(tex_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
            for line_count, line in enumerate(lines):
                result = re.findall(pattern, line, flags)
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


def main(check_dir):
    tex_paths = glob.glob(f"{check_dir}/**/*.tex",
                          recursive=True)
    checker_per_line = CheckerPerLine(tex_paths)

    # Check per line
    errors = checker_per_line.check(
        r"(?:^a|\sa) (?:[aiueo]|{\\it [aiueo])", re.IGNORECASE)
    print_log("'a' -> 'an'", "error", errors)

    errors = checker_per_line.check(
        r"(?:^an|\san) (?:[^aiueo]|{\\it [^aiueo])", re.IGNORECASE)
    print_log("'an' -> 'a'", "error", errors)


if __name__ == "__main__":
    check_dir = option_parser()
    main(check_dir)
