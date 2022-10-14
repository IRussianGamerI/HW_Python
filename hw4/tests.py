import unittest
from meta import CustomMeta
from desc import Integer, PositiveInteger, String


class CustomMetaTestCase(unittest.TestCase):
    def test_all(self):
        class TestClass(metaclass=CustomMeta):
            reg_attr = 11

            def __init__(self):
                self.fake_magic__ = 44

            def function(self):
                return 22

            def __str__(self):
                return 'STR'

        instance = TestClass()

        with self.assertRaises(AttributeError):
            print(instance.reg_attr)

        with self.assertRaises(AttributeError):
            print(instance.fake_magic__)

        with self.assertRaises(AttributeError):
            print(instance.function())

        self.assertTrue(hasattr(instance, 'custom_reg_attr'))
        self.assertTrue(hasattr(instance, 'custom_fake_magic__'))
        self.assertTrue(hasattr(instance, 'custom_function'))
        self.assertTrue(hasattr(instance, '__init__'))
        self.assertTrue(hasattr(instance, '__str__'))

        self.assertFalse(hasattr(instance, 'added_later'))
        self.assertFalse(hasattr(instance, 'custom_added_later'))
        instance.added_later = 'added_later'
        self.assertTrue(hasattr(instance, 'custom_added_later'))


class DescriptorsTestCase(unittest.TestCase):
    class Data:
        num = Integer()
        string = String()
        pos_num = PositiveInteger()

    data = Data()

    def test_int(self):
        self.assertEqual(self.data.num, 0)

        self.data.num = 1
        self.assertEqual(self.data.num, 1)

        self.data.num = -1
        self.assertEqual(self.data.num, -1)

        with self.assertRaises(TypeError):
            self.data.num = "string"
        self.assertEqual(self.data.num, -1)

        with self.assertRaises(TypeError):
            self.data.num = 2.0
        self.assertEqual(self.data.num, -1)

        self.data.num = False
        self.assertFalse(self.data.num)

        with self.assertRaises(TypeError):
            self.data.num = 2 + 2j
        self.assertFalse(self.data.num)

    def test_string(self):
        self.assertEqual(self.data.string, "")

        self.data.string = "new"
        self.assertEqual(self.data.string, "new")

        self.data.string = "changed"
        self.assertEqual(self.data.string, "changed")

        with self.assertRaises(TypeError):
            self.data.string = 1

        self.assertEqual(self.data.string, "changed")

    def test_pos_int(self):
        self.assertEqual(self.data.pos_num, 1)

        self.data.pos_num = 2
        self.assertEqual(self.data.pos_num, 2)

        self.data.pos_num = 22
        self.assertEqual(self.data.pos_num, 22)

        with self.assertRaises(TypeError):
            self.data.pos_num = "string"
        self.assertEqual(self.data.pos_num, 22)

        with self.assertRaises(TypeError):
            self.data.pos_num = 2.0
        self.assertEqual(self.data.pos_num, 22)

        with self.assertRaises(ValueError):
            self.data.pos_num = -1
        self.assertEqual(self.data.pos_num, 22)

        with self.assertRaises(ValueError):
            self.data.pos_num = 0
        self.assertEqual(self.data.pos_num, 22)

        self.data.num = True
        self.assertTrue(self.data.pos_num)

        with self.assertRaises(TypeError):
            self.data.pos_num = 2 + 2j
        self.assertTrue(self.data.pos_num)


if __name__ == "__main__":
    unittest.main()
