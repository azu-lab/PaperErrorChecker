import os

import yaml
from src.run_checker import Checker


class TestChecker:

    def test_get_target_path_dict(self, mocker):
        mocker.patch("glob.glob",
                     return_value=["XXX\\system_model.tex",
                                   "XXX\\Introduction.tex",
                                   "XXX\\Abstract.tex",
                                   "XXX\\Evaluation.tex"])

        target_path_dict = Checker._get_tex_path_dict("check_dir")
        assert ("XXX\\system_model.tex" in target_path_dict["all"]
                and "XXX\\Introduction.tex" in target_path_dict["all"]
                and "XXX\\Abstract.tex" in target_path_dict["all"]
                and "XXX\\Evaluation.tex" in target_path_dict["all"])
        assert "XXX\\Introduction.tex" in target_path_dict["introduction"]
        assert "XXX\\Abstract.tex" in target_path_dict["abstract"]
        assert ("XXX\\system_model.tex" in target_path_dict["except for abstract"]
                and "XXX\\Introduction.tex" in target_path_dict["except for abstract"]
                and "XXX\\Evaluation.tex" in target_path_dict["except for abstract"])

    def test_get_check_lists(self):
        with open(
            f"{os.path.dirname(__file__)}/../src/check_lists/common.yaml",
            "r"
        ) as f:
            common_list = yaml.safe_load(f)
        common_len = len(common_list)

        with open(
            f"{os.path.dirname(__file__)}/../src/check_lists/conference.yaml",
            "r"
        ) as f:
            conference_list = yaml.safe_load(f)
        conference_len = len(conference_list)

        with open(
            f"{os.path.dirname(__file__)}/../src/check_lists/thesis.yaml",
            "r"
        ) as f:
            thesis_list = yaml.safe_load(f)
        thesis_len = len(thesis_list)

        check_lists = Checker._get_check_lists("conference")
        assert len(check_lists) == common_len + conference_len

        check_lists = Checker._get_check_lists("thesis")
        assert len(check_lists) == common_len + thesis_len

    def test_perse_options(self, caplog):
        caplog.clear()
        options = {"pattern": 'XXX',
                   "level": "err",
                   "target": "all",
                   "flags": "ignorecase"}
        try:
            p, l, t, f = Checker._perse_options(options)
        except:
            assert ('Specify "error", "warning", '
                    'or "info" for "level".') in caplog.text

        caplog.clear()
        options = {"pattern": 'XXX',
                   "level": "error",
                   "flags": "ignorecase"}
        p, l, t, f = Checker._perse_options(options)
        assert t != "all"

        caplog.clear()
        options = {"pattern": 'XXX',
                   "level": "error",
                   "target": "alll",
                   "flags": "ignorecase"}
        try:
            p, l, t, f = Checker._perse_options(options)
        except:
            assert ('Specify "all", "introduction", "abstract", '
                    'or "except for abstract" for "target".') in caplog.text

        caplog.clear()
        options = {"pattern": 'XXX',
                   "level": "error",
                   "target": "all"}
        p, l, t, f = Checker._perse_options(options)
        assert f is None

        caplog.clear()
        options = {"pattern": 'XXX',
                   "level": "error",
                   "target": "all",
                   "flags": "ignorecas"}
        try:
            p, l, t, f = Checker._perse_options(options)
        except:
            assert ('Specify "ignorecase" for "flags".') in caplog.text
