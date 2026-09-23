"""Check sequential search results on unsorted inputs and boundary cases."""

import itertools
import unittest

from src.linear_search import linear_search


class LinearSearchTests(unittest.TestCase):
    def test_beginning_middle_and_end_of_unsorted_data(self):
        data = [7, 2, 9, 4, -3]
        for target, expected in [(7, 0), (9, 2), (-3, 4)]:
            with self.subTest(target=target):
                self.assertEqual(linear_search(data, target), expected)

    def test_missing_target(self):
        self.assertEqual(linear_search([7, 2, 9, 4], 5), -1)

    def test_empty_input(self):
        self.assertEqual(linear_search([], 1), -1)

    def test_one_element_found_and_missing(self):
        self.assertEqual(linear_search([0], 0), 0)
        self.assertEqual(linear_search([0], 1), -1)

    def test_duplicates_return_first_match(self):
        self.assertEqual(linear_search([5, 8, 5, 5], 5), 0)
        self.assertEqual(linear_search([8, 5, 5], 5), 1)

    def test_tuple_negative_and_zero_values(self):
        self.assertEqual(linear_search((4, -6, 0), -6), 1)
        self.assertEqual(linear_search((4, -6, 0), 0), 2)

    def test_found_and_missing_searches_leave_input_unchanged(self):
        data = [5, -1, 8, 5]
        before = data.copy()
        linear_search(data, 8)
        linear_search(data, 100)
        self.assertEqual(data, before)

    def test_small_inputs_agree_with_first_index_oracle(self):
        for size in range(5):
            for data in itertools.product((-2, 0, 3), repeat=size):
                for target in (-3, -2, 0, 3, 4):
                    with self.subTest(data=data, target=target):
                        expected = data.index(target) if target in data else -1
                        self.assertEqual(linear_search(data, target), expected)


if __name__ == "__main__":
    unittest.main()
