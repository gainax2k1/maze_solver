import unittest

from window import *  # needs to be adjusted
class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )
        # Test that zero dimensions raise an error
        with self.assertRaises(ValueError):
            m1 = Maze(0, 0, 0, 0, 10, 10)

        with self.assertRaises(ValueError):
            m2 = Maze(0, 0, -5, 10, 10, 10)


if __name__ == "__main__":
    unittest.main()
