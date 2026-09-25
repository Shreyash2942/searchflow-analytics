"""Exercise actual small benchmark runs and verify CSV/metadata consistency."""

import csv
import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from statistics import median
from unittest.mock import patch

import main
from src.benchmark import run_benchmarks
from src.data_generator import DATASET_SIZES, generate_required_datasets
from src.data_loader import load_dataset


class BenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.data = root / "data"
        self.output = root / "results"
        generate_required_datasets(self.data)

    def test_complete_run_records_real_samples_and_correct_results(self):
        before = {p.name: p.read_bytes() for p in self.data.glob("*.csv")}
        records = run_benchmarks(self.data, self.output, repeats=2, iterations=2, warmups=0)
        self.assertEqual(len(records), 24)
        metadata = json.loads((self.output / "benchmark_metadata.json").read_text())
        csv_bytes = (self.output / "performance_results.csv").read_bytes()
        self.assertEqual(metadata["csv_sha256"], hashlib.sha256(csv_bytes).hexdigest())
        self.assertEqual(len(metadata["measurements"]), 24)
        for size in DATASET_SIZES:
            subset = [row for row in records if row.dataset_size == size]
            self.assertEqual(len(subset), 8)
            self.assertEqual(sum(not row.found for row in subset), 2)
        for number, (row, measurement) in enumerate(zip(records, metadata["measurements"]), 1):
            self.assertEqual(measurement["csv_row"], number)
            self.assertEqual(measurement["target"], row.target)
            self.assertEqual(measurement["algorithm"], row.algorithm)
            self.assertEqual(len(measurement["batch_seconds_per_search"]), 2)
            self.assertEqual(median(measurement["batch_seconds_per_search"]), row.execution_time)
            self.assertGreaterEqual(row.execution_time, 0)
            data = load_dataset(self.data / f"dataset_{row.dataset_size}.csv")
            searched = data if row.algorithm == "Linear" else sorted(data)
            if row.found:
                self.assertEqual(searched[row.index], row.target)
            else:
                self.assertNotIn(row.target, searched)
        for dataset in metadata["datasets"]:
            self.assertEqual(dataset["sha256"], hashlib.sha256(before[dataset["file"]]).hexdigest())
            self.assertEqual(dataset["sort_seconds"], median(dataset["sort_samples_seconds"]))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.data.glob("*.csv")})
        with (self.output / "performance_results.csv").open(newline="") as stream:
            self.assertEqual(len(list(csv.DictReader(stream))), 24)

    def test_missing_dataset_leaves_previous_results_untouched(self):
        self.output.mkdir()
        path = self.output / "performance_results.csv"
        path.write_text("previous run")
        (self.data / "dataset_10000.csv").unlink()
        with self.assertRaises(FileNotFoundError):
            run_benchmarks(self.data, self.output, repeats=1, iterations=1, warmups=0)
        self.assertEqual(path.read_text(), "previous run")

    def test_invalid_settings_do_not_create_output(self):
        with self.assertRaises(ValueError):
            run_benchmarks(self.data, self.output, repeats=0)
        self.assertFalse(self.output.exists())

    def test_entry_point_runs_benchmark_with_custom_settings(self):
        output = io.StringIO()
        with patch.object(main, "DEFAULT_DATA_DIR", self.data), \
                patch.object(main, "DEFAULT_RESULTS_DIR", self.output), \
                patch("sys.argv", ["main.py", "--benchmark", "--repeats", "1", "--iterations", "2", "--warmups", "0"]), \
                redirect_stdout(output):
            self.assertEqual(main.main(), 0)
        self.assertIn("Saved 24 measurements", output.getvalue())
        metadata = json.loads((self.output / "benchmark_metadata.json").read_text())
        self.assertEqual(metadata["iterations_per_batch"], 2)

    def test_entry_point_reports_invalid_counts(self):
        errors = io.StringIO()
        with patch("sys.argv", ["main.py", "--benchmark", "--repeats", "0"]), \
                redirect_stderr(errors), redirect_stdout(io.StringIO()):
            self.assertEqual(main.main(), 1)
        self.assertIn("repeats", errors.getvalue())

    def test_timing_options_require_benchmark_flag(self):
        with patch("sys.argv", ["main.py", "--iterations", "10"]), \
                redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main.main()
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
