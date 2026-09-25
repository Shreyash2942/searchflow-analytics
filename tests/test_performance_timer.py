"""Verify timing arithmetic and boundaries with a controlled clock."""

import unittest
from unittest.mock import Mock, patch

from src.linear_search import linear_search
from src.performance_timer import time_search


class PerformanceTimerTests(unittest.TestCase):
    def test_reports_median_batch_mean_and_preserves_samples(self):
        search = Mock(return_value=0)
        with patch("src.performance_timer.perf_counter", side_effect=[0, 6, 10, 12, 20, 24]):
            result = time_search(search, [5], 5, repeats=3, iterations=2, warmups=2)
        self.assertEqual(result.index, 0)
        self.assertEqual(result.samples, (3.0, 1.0, 2.0))
        self.assertEqual(result.execution_time, 2.0)
        self.assertEqual(search.call_count, 1 + 2 + 3 * 2)

    def test_correctness_check_and_warmups_precede_timed_calls(self):
        events = []

        def search(data, target):
            events.append("search")
            return 0

        def clock():
            events.append("clock")
            return 1.0

        with patch("src.performance_timer.perf_counter", side_effect=clock):
            time_search(search, [1], 1, repeats=1, iterations=2, warmups=1)
        self.assertEqual(events, ["search", "search", "clock", "search", "search", "clock"])

    def test_missing_and_empty_inputs(self):
        for data in ([1, 2], []):
            with self.subTest(data=data), patch("src.performance_timer.perf_counter", side_effect=[1, 2]):
                result = time_search(linear_search, data, 3, repeats=1, iterations=1, warmups=0)
                self.assertEqual(result.index, -1)
                self.assertEqual(result.execution_time, 1)

    def test_invalid_settings_do_not_call_search(self):
        search = Mock()
        for options in ({"repeats": 0}, {"repeats": True}, {"iterations": -1},
                        {"iterations": 1.5}, {"warmups": -1}, {"warmups": False}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                time_search(search, [1], 1, **options)
        search.assert_not_called()

    def test_incorrect_search_results_rejected_before_clock(self):
        for index in (-2, 2, True, -1, 1):
            with self.subTest(index=index), patch("src.performance_timer.perf_counter") as clock:
                with self.assertRaises(ValueError):
                    time_search(lambda data, target: index, [7, 8], 7)
                clock.assert_not_called()

    def test_inconsistent_results_rejected(self):
        search = Mock(side_effect=[0, 1])
        with self.assertRaisesRegex(ValueError, "inconsistent"), \
                patch("src.performance_timer.perf_counter", side_effect=[1, 2]):
            time_search(search, [7, 7], 7, repeats=1, iterations=1, warmups=0)

    def test_invalid_clock_samples_rejected(self):
        for end in (-1, float("nan"), float("inf")):
            with self.subTest(end=end), patch("src.performance_timer.perf_counter", side_effect=[0, end]):
                with self.assertRaises(ValueError):
                    time_search(linear_search, [1], 1, repeats=1, iterations=1, warmups=0)


if __name__ == "__main__":
    unittest.main()
