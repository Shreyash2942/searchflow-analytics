"""Check sorted search correctness and bounded work without noisy time limits."""

import itertools
import unittest

from src.binary_search import binary_search


class IndexedReadCounter(list):
    """Count indexed reads to check the search's logarithmic work bound."""

    def __init__(self, values):
        super().__init__(values)
        self.reads = 0

    def __getitem__(self, index):
        self.reads += 1
        return super().__getitem__(index)


class BinarySearchTests(unittest.TestCase):
    def test_beginning_middle_and_end(self):
        data = [-8, -2, 0, 5, 9]
        for target, expected in [(-8, 0), (0, 2), (9, 4)]:
            with self.subTest(target=target):
                self.assertEqual(binary_search(data, target), expected)

    def test_missing_below_between_and_above_values(self):
        for target in (-10, 2, 20):
            with self.subTest(target=target):
                self.assertEqual(binary_search([-8, 0, 5, 9], target), -1)

    def test_empty_input(self):
        self.assertEqual(binary_search([], 0), -1)

    def test_one_and_two_element_inputs(self):
        for data in ([5], [1, 5]):
            for target in (0, 1, 5, 6):
                with self.subTest(data=data, target=target):
                    expected = data.index(target) if target in data else -1
                    self.assertEqual(binary_search(data, target), expected)

    def test_duplicates_return_a_matching_index(self):
        for data, target in [([1, 2, 2, 2, 7], 2), ([4] * 8, 4)]:
            with self.subTest(data=data):
                index = binary_search(data, target)
                self.assertGreaterEqual(index, 0)
                self.assertLess(index, len(data))
                self.assertEqual(data[index], target)

    def test_tuple_and_input_preservation(self):
        self.assertEqual(binary_search((-4, 0, 9), 0), 1)
        data = [-4, 0, 9]
        before = data.copy()
        binary_search(data, 9)
        binary_search(data, 20)
        self.assertEqual(data, before)

    def test_small_sorted_inputs_agree_with_membership_oracle(self):
        for size in range(7):
            for data in itertools.combinations_with_replacement((-2, 0, 3), size):
                for target in (-3, -2, -1, 0, 1, 3, 4):
                    with self.subTest(data=data, target=target):
                        index = binary_search(data, target)
                        if target in data:
                            self.assertGreaterEqual(index, 0)
                            self.assertLess(index, len(data))
                            self.assertEqual(data[index], target)
                        else:
                            self.assertEqual(index, -1)

    def test_indexed_reads_have_a_logarithmic_bound(self):
        for size in (1, 2, 3, 10, 100, 1_000, 10_000):
            for target in (-1, size - 1, size):
                with self.subTest(size=size, target=target):
                    data = IndexedReadCounter(range(size))
                    self.assertEqual(binary_search(data, target), target if target == size - 1 else -1)
                    self.assertLessEqual(data.reads, size.bit_length())

    def test_middle_match_requires_one_indexed_read(self):
        data = IndexedReadCounter(range(101))
        self.assertEqual(binary_search(data, 50), 50)
        self.assertEqual(data.reads, 1)


if __name__ == "__main__":
    unittest.main()
