import unittest
from lru_cache import LRUCache


class TestLruCache(unittest.TestCase):
    def test_creation(self):
        with self.assertRaises(TypeError):
            bad = LRUCache(0.5)

        with self.assertRaises(ValueError):
            bad = LRUCache(-294)

    def test_size_one(self):
        just_one = LRUCache(1)
        just_one.set("Only", "One")
        self.assertEqual(just_one.get("Only"), "One")
        just_one.set("New", "Two")
        self.assertEqual(just_one.get("Only"), None)
        self.assertEqual(just_one.get("New"), "Two")

    def test_update_just_before_displacement(self):
        four_dict = LRUCache(4)
        four_dict.set("one", 1)
        four_dict.set("two", 2)
        four_dict.set("three", 3)
        four_dict.set("four", 4)
        self.assertEqual(four_dict.get("one"), 1)
        self.assertEqual(four_dict.get("two"), 2)
        self.assertEqual(four_dict.get("three"), 3)
        self.assertEqual(four_dict.get("four"), 4)
        four_dict.set("one", 1)  # renew
        four_dict.set("five", 5)
        self.assertEqual(four_dict.get("two"), None)  # deleted
        self.assertEqual(four_dict.get("one"), 1)
        self.assertEqual(four_dict.get("five"), 5)  # recently added
        self.assertEqual(four_dict.get("three"), 3)
        self.assertEqual(four_dict.get("four"), 4)

    def test_default(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k3"), None)  # None
        self.assertEqual(cache.get("k2"), "val2")  # "val2"
        self.assertEqual(cache.get("k1"), "val1")  # "val1"

        cache.set("k3", "val3")

        self.assertEqual(cache.get("k3"), "val3")  # "val3"
        self.assertEqual(cache.get("k2"), None)  # None
        self.assertEqual(cache.get("k1"), "val1")  # "val1"


if __name__ == "__main__":
    unittest.main()
