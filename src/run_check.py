import argparse
import glob
import os
import re
from logging import INFO, Formatter, StreamHandler, getLogger
from typing import List

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


def main(check_dir):
    tex_paths = glob.glob(f"{check_dir}/**/*.tex",
                          recursive=True)
    checker_per_line = CheckerPerLine(tex_paths)

    # Check per line
    # ERROR
    errors = checker_per_line.check(
        r"(?:^a|\sa) (?:[aiueo]|{\\it [aiueo])", re.IGNORECASE)
    print_log("'a' -> 'an'", "error", errors)

    errors = checker_per_line.check(
        r"(?:^an|\san) (?:[^aiueo]|{\\it [^aiueo])", re.IGNORECASE)
    print_log("'an' -> 'a'", "error", errors)

    errors = checker_per_line.check(
        r"\\cite{\w+}, \\cite")
    print_log("'\\cite{X}, \\cite{Y}' -> \\cite{X, Y}", "error", errors)

    errors = checker_per_line.check(
        r"et al[^\.]|Fig[^u\.]|Eq[^s\.]|Eqs[^\.]")
    print_log("Insert a period", "error", errors)

    errors = checker_per_line.check(
        r"However |In addition |Additionally |Therefore |Here |Otherwise |"
        r"e\.g\. |i\.e\. |"
        r" [0-9]{4,}"
    )
    print_log("Insert a comma", "error", errors)

    errors = checker_per_line.check(
        r"[0-9]+ms|\w\\cite|ROS2")
    print_log("Insert a half-width space", "error", errors)

    errors = checker_per_line.check(
        r"(?:Fig\.|Figs\.|Figure\.|Figures\.|Eq\.|Eqs\.|"
        r"Table\.|Tables\.|Algorithm\.|Algorithms\.)[^~]")
    print_log("Insert a tilde", "error", errors)

    errors = checker_per_line.check(
        r"[0-9]+ %|\w :")
    print_log("Remove a half-width space", "error", errors)

    errors = checker_per_line.check(
        r"each (?:a|an|the)|"
        r"(?:[aA]|[aA]n|[tT]he) (?:Fig|Table|Eq|Algorithm|Section)")
    print_log("Remove an article", "error", errors)

    errors = checker_per_line.check(
        r"(?:are|is) (?:existing|having)|"
        r", (?:however|therefore|then|thus|thereby)")
    print_log("Grammar errors", "error", errors)

    errors = checker_per_line.check(
        r"works")
    print_log("Uncountable noun", "error", errors)

    errors = checker_per_line.check(
        r"==")
    print_log("'==' -> '='", "error", errors)

    errors = checker_per_line.check(
        r"<=|>=")
    print_log("'<=' or '>=' -> '\\leq' or '\\geq'", "error", errors)

    errors = checker_per_line.check(
        r"Acknowledgements")
    print_log("'Acknowledgements' -> 'Acknowledgments'", "error", errors)

    errors = checker_per_line.check(
        r"self-driving card")
    print_log("'self-driving car' -> 'autonomous vehicles'", "error", errors)

    errors = checker_per_line.check(
        r"was proposed")
    print_log("'was proposed' -> 'has been proposed'", "error", errors)

    errors = checker_per_line.check(
        r"GPS")
    print_log("'GPS' -> 'Global Navigation Satellite System (GNSS)'",
              "error", errors)

    # WARNING
    errors = checker_per_line.check(
        r"don't|hasn't|doesn't|can't|"
        r"so|very| etc|think|"
        r"elderly people|man[\s\.]|men[\s\.]|women|women|"
        r"it is|there (?:is|are)|you|people|"
        r"several|good|get |"
        r"we |(?:^| )I |"
        r"previous work",
        re.IGNORECASE)
    print_log("Don't use", "warning", errors)
    errors = checker_per_line.check(
        r"And|But|Also")
    print_log("Don't use", "warning", errors)
    errors = checker_per_line.check(
        r"resent")
    print_log("Don't use 'resent' in except for abstract", "warning", errors)

    errors = checker_per_line.check(
        r" [0-9] ")
    print_log("Spell out", "warning", errors)

    errors = checker_per_line.check(
        r"a lot of")
    print_log("'a lot of' -> 'many' or 'much'", "warning", errors)

    # INFO
    errors = checker_per_line.check(
        r"about")
    print_log("'about' -> 'approximately'", "info", errors)

    errors = checker_per_line.check(
        r"correctly")
    print_log("'correctly' -> 'accurately'", "info", errors)

    errors = checker_per_line.check(
        r"purpose")
    print_log("'purpose' -> 'objective'", "info", errors)


if __name__ == "__main__":
    check_dir = option_parser()
    main(check_dir)
