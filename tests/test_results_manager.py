"""Verify CSV schema, precision, found/index semantics and invalid output handling."""

import csv
import tempfile
import unittest
from pathlib import Path

from src.results_manager import BenchmarkResult, RESULT_COLUMNS, save_results


class ResultsManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "nested" / "results.csv"

    def test_round_trip_exact_schema_and_timing_precision(self):
        records = [BenchmarkResult("Linear", 100, 7, True, 0, 1.23456789e-7),
                   BenchmarkResult("Binary", 100, 999, False, -1, 0.0)]
        save_results(records, self.path)
        self.assertNotIn(b"\r", self.path.read_bytes())
        with self.path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            self.assertEqual(reader.fieldnames, list(RESULT_COLUMNS))
            rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["found"], "True")
        self.assertEqual(rows[0]["index"], "0")
        self.assertEqual(float(rows[0]["execution_time"]), records[0].execution_time)
        self.assertEqual(rows[1]["found"], "False")

    def test_invalid_records_rejected(self):
        valid = dict(algorithm="Linear", dataset_size=100, target=7, found=True, index=0, execution_time=0.01)
        for changes in ({"algorithm": "Other"}, {"dataset_size": 0}, {"target": True},
                        {"found": False}, {"index": 100}, {"index": -2},
                        {"execution_time": -1}, {"execution_time": float("nan")},
                        {"execution_time": float("inf")}, {"execution_time": True}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                BenchmarkResult(**(valid | changes))

    def test_empty_or_wrong_record_input_preserves_existing_file(self):
        save_results([BenchmarkResult("Linear", 1, 7, True, 0, 1e-6)], self.path)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            save_results([], self.path)
        with self.assertRaises(TypeError):
            save_results([{}], self.path)
        self.assertEqual(self.path.read_bytes(), before)

    def test_repeated_export_replaces_rows_without_duplicate_headers(self):
        row = BenchmarkResult("Linear", 1, 7, True, 0, 0.1)
        save_results([row, row], self.path)
        save_results([row], self.path)
        self.assertEqual(len(self.path.read_text().splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
