import unittest
from arraysum import sum


class TestSum(unittest.TestCase):
    known_values = (([31, -41, 59, 26, -53, 58, 97, -93, -23, 84][2:7], 187),
                    ([-2, -1, 1, 2, 0, -1, 7][2:7], 9),
                    ([-2, -1, 1, 2, -8, -1, 7][2:4], 3),
                    ([-1, -2, -3, -4, 0], 0),
                    ([-1, -2, -3, -4, 0, 1], 1))

    def test_sum(self):
        """
        Should give known result with known input
        """
        for alist, answer in self.known_values:
            result = sum(alist)
            self.assertEqual(answer, result)


if __name__ == '__main__':
    unittest.main()
