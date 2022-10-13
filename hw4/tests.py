import unittest
from meta import CustomMeta


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
