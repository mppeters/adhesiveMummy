import unittest
import Main

# """
# Here are all the possible methods we can use for our tests:

# assertEquals(a, b) --> a = b
# assertNotEqual(a, b) --> a != b
# assertTrue(x) --> bool(x) is True
# assertFalse(x) --> bool(x) is False
# assertIs(a, b) --> a is b
# assertIsNot(a, b) --> a is not b
# 3assertIsNone(x) --> x is None
# assertIn(a, b) --> a in b
# assertNotIn(a, b) --> a not in b
# assertIsInstance(a, b) --> isinstance(a, b)
# assertNotIsInstance(a, b)  --> not isinstance(a, b)

# """

# below is the structure for creating tests using a simple addition function as an example


class testAdd(unittest.TestCase):
    def test_add(self):
        self.assertEqual(Main.add(2, 4), 6)
        self.assertEqual(Main.add(-1, 1), 0)
        self.assertEqual(Main.add(-1, -1), -2)
        self.assertEqual(Main.add(0, -1), -1)


if __name__ == '__main__':
    unittest.main()
