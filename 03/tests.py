import unittest
from unittest import TestCase
from custom_list import CustomList


class TestCustomList(TestCase):
    def assert_equal_cl(self, clist1, clist2):
        self.assertEqual(len(clist1), len(clist2))
        for item1, item2 in zip(clist1, clist2):
            self.assertEqual(item1, item2)

    def test_eq(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertTrue(clist1 == clist2)

        clist2 = CustomList([3, 0, 0])
        self.assertTrue(clist1 == clist2)

        clist2 = CustomList([0, 1, 0])
        self.assertFalse(clist1 == clist2)

    def test_ne(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertFalse(clist1 != clist2)

        clist2 = CustomList([0, 3, 0])
        self.assertFalse(clist1 != clist2)

        clist2 = CustomList([0, 1, 0])
        self.assertTrue(clist1 != clist2)

    def test_lt(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertFalse(clist1 < clist2)

        clist2 = CustomList([1, 2, 3, 1])
        self.assertTrue(clist1 < clist2)

        clist2 = CustomList([1, 2, 4, -3])
        self.assertTrue(clist1 < clist2)

    def test_le(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertTrue(clist1 <= clist2)

        clist2 = CustomList([1, 2, 2, 1])
        self.assertTrue(clist1 <= clist2)

        clist2 = CustomList([1, 0, 1])
        self.assertFalse(clist1 <= clist2)

    def test_gt(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertFalse(clist1 > clist2)

        clist2 = CustomList([1, 0, 1])
        self.assertTrue(clist1 > clist2)

        clist2 = CustomList([5, 4, 8, -3])
        self.assertFalse(clist1 > clist2)

    def test_ge(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, 2])
        self.assertTrue(clist1 >= clist2)

        clist2 = CustomList([0, 2, 0])
        self.assertTrue(clist1 >= clist2)

        clist2 = CustomList([1, 2, -2, 3])
        self.assertFalse(clist1 >= clist2)

    def test_str(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, -2])

        self.assertEqual(str(clist1), "[0, 1, 2] 3")
        self.assertEqual(str(clist2), "[0, 1, -2] -1")

    def test_add_clist_to_clist(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, -2])
        list_sum = clist1 + clist2

        self.assert_equal_cl(list_sum, CustomList([0, 2, 0]))
        self.assert_equal_cl(clist1, CustomList([0, 1, 2]))
        self.assert_equal_cl(clist2, CustomList([0, 1, -2]))

        clist1 = CustomList([0, 1, 2, 3])
        clist2 = CustomList([-1, -2])
        list_sum = clist1 + clist2

        self.assert_equal_cl(list_sum, CustomList([-1, -1, 2, 3]))
        self.assert_equal_cl(clist1, CustomList([0, 1, 2, 3]))
        self.assert_equal_cl(clist2, CustomList([-1, -2]))

        clist1 = CustomList([0, 1, 2, 4])
        clist2 = CustomList([-1, -2, -3])
        list_sum = clist2 + clist1

        self.assert_equal_cl(list_sum, CustomList([-1, -1, -1, 4]))
        self.assert_equal_cl(clist1, CustomList([0, 1, 2, 4]))
        self.assert_equal_cl(clist2, CustomList([-1, -2, -3]))

    def test_clist_plus_list(self):
        clist = CustomList([0, 1, 2])
        std_list = list([0, 1, -2])
        list_sum = clist + std_list

        self.assert_equal_cl(list_sum, CustomList([0, 2, 0]))
        self.assert_equal_cl(clist, CustomList([0, 1, 2]))
        self.assert_equal_cl(std_list, [0, 1, -2])
        self.assertIsInstance(list_sum, CustomList)

        clist = CustomList([0, 1, 2, 1])
        std_list = list([0, 1])
        list_sum = clist + std_list

        self.assert_equal_cl(list_sum, CustomList([0, 2, 2, 1]))
        self.assert_equal_cl(clist, CustomList([0, 1, 2, 1]))
        self.assert_equal_cl(std_list, [0, 1])
        self.assertIsInstance(list_sum, CustomList)

    def test_list_plus_clist(self):
        std_list = list([0, 1, -2])
        clist = CustomList([0, 1, 2])
        list_sum = std_list + clist

        self.assert_equal_cl(list_sum, CustomList([0, 2, 0]))
        self.assert_equal_cl(std_list, [0, 1, -2])
        self.assert_equal_cl(clist, CustomList([0, 1, 2]))
        self.assertIsInstance(list_sum, CustomList)

        std_list = list([-1, 4])
        clist = CustomList([1, 2, 3, -5])
        list_sum = std_list + clist

        self.assert_equal_cl(list_sum, CustomList([0, 6, 3, -5]))
        self.assert_equal_cl(std_list, [-1, 4])
        self.assert_equal_cl(clist, CustomList([1, 2, 3, -5]))
        self.assertIsInstance(list_sum, CustomList)

    def test_sub_clist_from_clist(self):
        clist1 = CustomList([0, 1, 2])
        clist2 = CustomList([0, 1, -2])
        list_sub = clist1 - clist2

        self.assert_equal_cl(list_sub, CustomList([0, 0, 4]))
        self.assert_equal_cl(clist1, CustomList([0, 1, 2]))
        self.assert_equal_cl(clist2, CustomList([0, 1, -2]))

        clist1 = CustomList([0, 1])
        clist2 = CustomList([1, 2, 3, 4])
        list_sub = clist1 - clist2

        self.assert_equal_cl(list_sub, CustomList([-1, -1, -3, -4]))
        self.assert_equal_cl(clist1, CustomList([0, 1]))
        self.assert_equal_cl(clist2, CustomList([1, 2, 3, 4]))

        list_sub = clist2 - clist1

        self.assert_equal_cl(list_sub, CustomList([1, 1, 3, 4]))
        self.assert_equal_cl(clist1, CustomList([0, 1]))
        self.assert_equal_cl(clist2, CustomList([1, 2, 3, 4]))

    def test_clist_minus_list(self):
        clist = CustomList([0, 1, 2])
        std_list = list([0, 1, -2])
        list_sub = clist - std_list

        self.assert_equal_cl(list_sub, CustomList([0, 0, 4]))
        self.assert_equal_cl(clist, CustomList([0, 1, 2]))
        self.assert_equal_cl(std_list, [0, 1, -2])
        self.assertIsInstance(list_sub, CustomList)

        clist = CustomList([1, 2, 3, 4])
        std_list = list([1, 2])
        list_sub = clist - std_list

        self.assert_equal_cl(list_sub, CustomList([0, 0, 3, 4]))
        self.assert_equal_cl(clist, CustomList([1, 2, 3, 4]))
        self.assert_equal_cl(std_list, [1, 2])
        self.assertIsInstance(list_sub, CustomList)

    def test_list_minus_clist(self):
        std_list = list([0, 1, -2])
        clist = CustomList([0, 1, 2])
        list_sub = std_list - clist

        self.assert_equal_cl(list_sub, CustomList([0, 0, -4]))
        self.assert_equal_cl(std_list, [0, 1, -2])
        self.assert_equal_cl(clist, CustomList([0, 1, 2]))
        self.assertIsInstance(list_sub, CustomList)

        std_list = list([-1, 4])
        clist = CustomList([1, 2, 3, -4])
        list_sub = std_list - clist

        self.assert_equal_cl(list_sub, CustomList([-2, 2, -3, 4]))
        self.assert_equal_cl(std_list, [-1, 4])
        self.assert_equal_cl(clist, CustomList([1, 2, 3, -4]))
        self.assertIsInstance(list_sub, CustomList)


if __name__ == "__main__":
    unittest.main()
