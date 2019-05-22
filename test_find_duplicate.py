import unittest
from find_duplicate import find_duplicate

class TestFindDuplicate(unittest.TestCase):

    def test_find_duplicate(self):
        '''Test find_duplicate function'''
        self.assertEqual(find_duplicate('ABGDDBEBSGGA'),'D')

if __name__ == '__main__':
    unittest.main()
