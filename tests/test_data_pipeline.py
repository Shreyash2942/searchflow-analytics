"""Verify Day 2 generation, file boundaries, validation, and independent copies."""

import io
import random
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main
from src.data_generator import (
    DATASET_SIZES,
    generate_dataset,
    generate_required_datasets,
    save_dataset,
)
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data, validate_dataset
from src.linear_search import linear_search
from src.binary_search import binary_search


class GenerationTests(unittest.TestCase):
    def test_required_sizes_are_reproducible_and_in_range(self):
        for size in DATASET_SIZES:
            with self.subTest(size=size):
                data = generate_dataset(size)
                self.assertEqual(len(data), size)
                self.assertTrue(all(type(value) is int and 0 <= value <= 100_000 for value in data))
                self.assertEqual(data, generate_dataset(size))

    def test_generation_does_not_change_global_random_state(self):
        state = random.getstate()
        generate_dataset(100)
        self.assertEqual(random.getstate(), state)

    def test_custom_bounds_and_duplicates(self):
        self.assertEqual(generate_dataset(4, min_value=-3, max_value=-3), [-3] * 4)

    def test_invalid_generation_settings(self):
        cases = [dict(size=0), dict(size=-1), dict(size=True), dict(size=1.5),
                 dict(size=2, seed=None), dict(size=2, min_value=True),
                 dict(size=2, max_value=1.2), dict(size=2, min_value=3, max_value=2)]
        for settings in cases:
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                generate_dataset(**settings)


class ProcessingTests(unittest.TestCase):
    def test_sorted_copy_preserves_values_duplicates_and_original_order(self):
        data = [7, -2, 7, 0]
        original, ordered = prepare_search_data(data, expected_size=4)
        self.assertEqual(original, [7, -2, 7, 0])
        self.assertEqual(ordered, [-2, 0, 7, 7])
        self.assertEqual(data, [7, -2, 7, 0])
        original[0] = 99
        ordered[0] = 88
        self.assertEqual(data, [7, -2, 7, 0])
        self.assertEqual(original[1], -2)
        self.assertEqual(ordered[-1], 7)

    def test_one_element_and_tuple(self):
        self.assertEqual(prepare_search_data((5,), expected_size=1), ([5], [5]))

    def test_invalid_contents(self):
        for data in ([], [True], [1.0], ["1"], [None], [float("nan")]):
            with self.subTest(data=data), self.assertRaises(ValueError):
                prepare_search_data(data)

    def test_nonsequence_rejected(self):
        for data in ("123", None, 123):
            with self.subTest(data=data), self.assertRaises(TypeError):
                validate_dataset(data)

    def test_count_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Expected 3 values, found 2"):
            prepare_search_data([1, 2], expected_size=3)

    def test_invalid_expected_count(self):
        for size in (0, -1, True, 2.0):
            with self.subTest(size=size), self.assertRaises(ValueError):
                validate_dataset([1, 2], expected_size=size)


class CsvPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.path = self.directory / "dataset.csv"

    def test_round_trip_and_parent_creation(self):
        destination = self.directory / "nested" / "dataset.csv"
        save_dataset([9, -4, 9, 0], destination)
        self.assertEqual(destination.read_text().splitlines()[0], "value")
        self.assertEqual(load_dataset(destination, expected_size=4), [9, -4, 9, 0])

    def test_invalid_save_preserves_existing_file(self):
        save_dataset([8], self.path)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            save_dataset([True], self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_bom_signed_integers_and_whitespace(self):
        self.path.write_text("value\n +12 \n-4\n0\n", encoding="utf-8-sig")
        self.assertEqual(load_dataset(self.path), [12, -4, 0])

    def test_invalid_csv_content(self):
        cases = {
            "empty file": "",
            "header only": "value\n",
            "wrong header": "number\n1\n",
            "no header": "1\n2\n",
            "extra header column": "value,other\n1,2\n",
            "extra data column": "value\n1,2\n",
            "blank row": "value\n1\n\n2\n",
            "blank cell": 'value\n""\n',
            "decimal": "value\n1.5\n",
            "text": "value\nhello\n",
            "underscore": "value\n1_000\n",
            "bad quotes": 'value\n"12\n',
        }
        for name, content in cases.items():
            with self.subTest(case=name):
                self.path.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_dataset(self.path)

    def test_invalid_encoding(self):
        self.path.write_bytes(b"value\n\xff\n")
        with self.assertRaisesRegex(ValueError, "invalid UTF-8 CSV"):
            load_dataset(self.path)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_dataset(self.path)

    def test_filesystem_error_is_preserved(self):
        with self.assertRaises(OSError):
            load_dataset(self.directory)

    def test_loaded_count_must_match(self):
        save_dataset([3, 1], self.path)
        with self.assertRaises(ValueError):
            load_dataset(self.path, expected_size=100)

    def test_all_required_files_round_trip_and_regenerate_identically(self):
        paths = generate_required_datasets(self.directory)
        self.assertEqual([path.name for path in paths], [f"dataset_{n}.csv" for n in DATASET_SIZES])
        before = [path.read_bytes() for path in paths]
        for size, path in zip(DATASET_SIZES, paths):
            with self.subTest(size=size):
                loaded = load_dataset(path, expected_size=size)
                original, ordered = prepare_search_data(loaded, expected_size=size)
                self.assertEqual(original, generate_dataset(size))
                self.assertEqual(ordered, sorted(original))
                self.assertEqual(loaded, original)
        generate_required_datasets(self.directory)
        self.assertEqual([path.read_bytes() for path in paths], before)

    def test_entry_point_reports_missing_file_without_traceback(self):
        errors = io.StringIO()
        with patch.object(main, "DEFAULT_DATA_DIR", self.directory), \
                patch("sys.argv", ["main.py"]), redirect_stderr(errors), \
                redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 1)
        self.assertIn("--generate", errors.getvalue())

    def test_searches_use_original_and_sorted_data_at_all_required_sizes(self):
        paths = generate_required_datasets(self.directory)
        for size, path in zip(DATASET_SIZES, paths):
            with self.subTest(size=size):
                loaded = load_dataset(path, expected_size=size)
                before = loaded.copy()
                original, ordered = prepare_search_data(loaded, expected_size=size)
                for target in (original[0], original[size // 2], original[-1], -1):
                    with self.subTest(target=target):
                        linear_index = linear_search(original, target)
                        binary_index = binary_search(ordered, target)
                        if target == -1:  # Generated values are nonnegative.
                            self.assertEqual((linear_index, binary_index), (-1, -1))
                        else:
                            self.assertGreaterEqual(linear_index, 0)
                            self.assertGreaterEqual(binary_index, 0)
                            self.assertEqual(original[linear_index], target)
                            self.assertEqual(ordered[binary_index], target)
                self.assertEqual(loaded, before)
                self.assertEqual(original, before)
                self.assertEqual(ordered, sorted(before))

    def test_entry_point_generates_and_validates(self):
        output = io.StringIO()
        with patch.object(main, "DEFAULT_DATA_DIR", self.directory), \
                patch("sys.argv", ["main.py", "--generate"]), redirect_stdout(output):
            self.assertEqual(main.main(), 0)
        self.assertIn("10,000 integers validated", output.getvalue())
        self.assertTrue((self.directory / "dataset_10000.csv").exists())


if __name__ == "__main__":
    unittest.main()
