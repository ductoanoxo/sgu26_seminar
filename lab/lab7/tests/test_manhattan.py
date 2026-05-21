import unittest

import pandas as pd

from src.manhattan import get_manhattan_distance


class TestManhattanDistance(unittest.TestCase):
    def test_distance_with_integer_values(self):
        df1 = pd.DataFrame([[1, 2], [3, 4]])
        df2 = pd.DataFrame([[2, 0], [1, 3]])

        self.assertEqual(get_manhattan_distance(df1, df2), 6.0)

    def test_distance_with_float_values(self):
        df1 = pd.DataFrame([[1.5, -2.0, 3], [0, 7.2, -1]])
        df2 = pd.DataFrame([[0.5, -1.0, 1], [0, 5.2, 2]])

        self.assertEqual(get_manhattan_distance(df1, df2), 9.0)

    def test_shape_mismatch_raises_value_error(self):
        df1 = pd.DataFrame([[1, 2], [3, 4]])
        df2 = pd.DataFrame([[1, 2, 3]])

        with self.assertRaises(ValueError):
            get_manhattan_distance(df1, df2)

    def test_non_numeric_data_raises_type_error(self):
        df1 = pd.DataFrame([[1, 2], [3, 4]])
        df2 = pd.DataFrame([["x", 0], [1, 3]])

        with self.assertRaises(TypeError):
            get_manhattan_distance(df1, df2)


if __name__ == "__main__":
    unittest.main()
