import unittest
from find_unique import find_unique

class TestFindUnique(unittest.TestCase):

    def test_find_unique(self):
        '''Test find_unique function'''
        self.assertEqual(find_unique('ABGDDBEBSGGA'),'E')

    def test_find_unique_when_none(self):
        '''Test find_unique function'''
        self.assertEqual(find_unique('ABGDDBEBESGSGA'), None)    

if __name__ == '__main__':
    unittest.main()
