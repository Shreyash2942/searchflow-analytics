"""Exercise the complete interactive workflow and preserve batch commands."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from src.cli import run_interactive, search_dataset
from src.data_generator import DATASET_SIZES, generate_required_datasets
from src.data_loader import load_dataset
from src.performance_timer import time_search


class InteractiveCliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / "data"
        generate_required_datasets(self.data)

    def session(self, answers):
        output, errors = io.StringIO(), io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output), redirect_stderr(errors):
            status = run_interactive(self.data)
        return status, output.getvalue(), errors.getvalue()

    def test_all_sizes_and_modes_use_correct_input_order(self):
        def quick_timing(search, values, target):
            return time_search(search, values, target, repeats=1, iterations=1, warmups=0)

        for size in DATASET_SIZES:
            values = load_dataset(self.data / f"dataset_{size}.csv")
            for mode, names in (("linear", ["Linear"]), ("binary", ["Binary"]),
                                ("both", ["Linear", "Binary"])):
                with self.subTest(size=size, mode=mode), patch("src.cli.time_search", side_effect=quick_timing):
                    rows = search_dataset(size, values[0], mode, self.data)
                    self.assertEqual([row.algorithm for row in rows], names)
                    for row in rows:
                        self.assertTrue(row.found)
                        searched = values if row.algorithm == "Linear" else sorted(values)
                        self.assertEqual(searched[row.index], values[0])
                        if row.algorithm == "Linear":
                            self.assertEqual(row.index, 0)

    def test_compare_both_displays_found_zero_index_order_and_time(self):
        target = load_dataset(self.data / "dataset_100.csv")[0]
        status, output, errors = self.session(["1", str(target), "3", "q"])
        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("LINEAR SEARCH", output)
        self.assertIn("BINARY SEARCH", output)
        self.assertEqual(output.count("Found: Yes"), 2)
        self.assertIn("Index: 0 (original-order data", output)
        self.assertIn("(sorted data, zero-based)", output)
        self.assertEqual(output.count("seconds/search"), 2)

    def test_negative_missing_target_and_single_mode(self):
        status, output, errors = self.session(["3", "-1", "2", "q"])
        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertIn("Dataset size: 10,000", output)
        self.assertIn("Target value: -1", output)
        self.assertIn("Found: No", output)
        self.assertIn("Index: -1 (not found)", output)
        self.assertNotIn("LINEAR SEARCH", output)

    def test_invalid_input_reprompts_and_zero_is_a_target(self):
        status, output, errors = self.session(["", "9", " 1 ", "abc", "1.5", "1_000",
                                               " +0 ", "bad", "0", " 1 ", "Q"])
        self.assertEqual(status, 0)
        self.assertEqual(errors, "")
        self.assertEqual(output.count("Invalid option."), 4)
        self.assertEqual(output.count("Enter a whole number"), 3)
        self.assertIn("Target value: 0", output)

    def test_integer_conversion_errors_reprompt_without_crash(self):
        with patch("src.cli.int", side_effect=ValueError("integer conversion limit"), create=True):
            status, output, _ = self.session(["1", "9" * 5000, "q"])
        self.assertEqual(status, 0)
        self.assertIn("Enter a whole number", output)

    def test_quit_at_each_prompt(self):
        for answers in (["q"], ["1", "q"], ["1", "7", "q"]):
            with self.subTest(answers=answers):
                status, output, errors = self.session(answers)
                self.assertEqual((status, errors), (0, ""))
                self.assertIn("Goodbye.", output)
                self.assertNotIn("Execution time:", output)

    def test_eof_and_interrupt_at_each_prompt(self):
        for interrupt in (EOFError, KeyboardInterrupt):
            for prefix in ([], ["1"], ["1", "7"]):
                with self.subTest(interrupt=interrupt, prefix=prefix):
                    status, output, errors = self.session([*prefix, interrupt()])
                    self.assertEqual((status, errors), (0, ""))
                    self.assertIn("Search session ended.", output)

    def test_multiple_searches_in_one_session(self):
        status, output, errors = self.session(["1", "-1", "1", "2", "-1", "2", "q"])
        self.assertEqual((status, errors), (0, ""))
        self.assertEqual(output.count("Found: No"), 2)

    def test_missing_file_recovers_to_menu_and_can_search_another_size(self):
        (self.data / "dataset_100.csv").unlink()
        status, output, errors = self.session(["1", "7", "1", "2", "-1", "2", "q"])
        self.assertEqual(status, 0)
        self.assertIn("--generate", errors)
        self.assertIn("Dataset size: 1,000", output)
        self.assertIn("Found: No", output)

    def test_malformed_csv_and_wrong_count_recover_without_traceback(self):
        for content in ("value\ninvalid\n", "value\n1\n"):
            with self.subTest(content=content):
                (self.data / "dataset_100.csv").write_text(content)
                status, output, errors = self.session(["1", "7", "3", "q"])
                self.assertEqual(status, 0)
                self.assertIn("Unable to search this dataset", errors)
                self.assertNotIn("Traceback", errors)
                self.assertIn("Goodbye.", output)

    def test_search_session_does_not_modify_or_create_files(self):
        root = self.data.parent
        before = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        self.session(["1", "-1", "3", "q"])
        after = {p.relative_to(root): p.read_bytes() for p in root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_invalid_direct_search_parameters(self):
        for size, target, mode in ((99, 1, "both"), (True, 1, "linear"),
                                  (100, True, "linear"), (100, 1, "other")):
            with self.subTest(size=size, target=target, mode=mode), self.assertRaises(ValueError):
                search_dataset(size, target, mode, self.data)

    def test_default_and_explicit_interactive_entry_point(self):
        for arguments in (["main.py"], ["main.py", "--interactive"]):
            with self.subTest(arguments=arguments), patch("sys.argv", arguments), \
                    patch("main.run_interactive", return_value=0) as menu, redirect_stdout(io.StringIO()):
                self.assertEqual(main.main(), 0)
                menu.assert_called_once_with(main.DEFAULT_DATA_DIR)

    def test_preview_remains_noninteractive(self):
        with patch("sys.argv", ["main.py", "--preview"]), \
                patch.object(main, "DEFAULT_DATA_DIR", self.data), \
                patch("builtins.input") as prompt, redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 0)
            prompt.assert_not_called()

    def test_generate_can_explicitly_launch_menu(self):
        with patch("sys.argv", ["main.py", "--generate", "--interactive"]), \
                patch.object(main, "DEFAULT_DATA_DIR", self.data), \
                patch("main.run_interactive", return_value=0) as menu, redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 0)
            menu.assert_called_once_with(self.data)

    def test_conflicting_actions_rejected(self):
        with patch("sys.argv", ["main.py", "--interactive", "--benchmark"]), \
                redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main.main()
        self.assertEqual(caught.exception.code, 2)

    def test_invalid_benchmark_settings_do_not_regenerate_data(self):
        with patch("sys.argv", ["main.py", "--generate", "--benchmark", "--repeats", "0"]), \
                patch("main.generate_required_datasets") as generate, \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main.main(), 1)
            generate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
