import unittest
from io import StringIO

from filter_file import filter_file


class TestFilterFile(unittest.TestCase):
    def test_exception(self):
        with self.assertRaises(TypeError):
            for line in filter_file(19, ['Тык-тык']):
                print(line)
        with self.assertRaises(TypeError):
            for line in filter_file('filename', 'word'):
                print(line)
        with self.assertRaises(ValueError):
            for line in filter_file('filename', ['word1', 'word2', 1337]):
                print(line)

    def test_file_object(self):
        file = StringIO("""Блах блах блах лютик Корусант розмарин
Роза
Азор
Розарио Доусон
Раздор
а Роза упала на лапу Азора
Миллион миллион миллион алых роз
Из окна из окна видишь ты
Кто влюблен кто влюблен кто влюблен и всерьез
Свою жизнь для тебя превратит в цветы
оХ аЗОР ох АзОр Ох Азор ты влюблен подарю подарю я тебе розЫ
А азорУ""")
        a = filter_file(file, ["РозА", "азоР"])
        self.assertEqual(next(a), "Роза")
        self.assertEqual(next(a), "Азор")
        self.assertEqual(next(a), "а Роза упала на лапу Азора")
        self.assertEqual(next(a), "оХ аЗОР ох АзОр Ох Азор ты влюблен подарю подарю я тебе розЫ")

    def test_filename(self):
        a = filter_file("test_file", ["РозА", "азоР"])
        self.assertEqual(next(a), "Роза")
        self.assertEqual(next(a), "Азор")
        self.assertEqual(next(a), "а Роза упала на лапу Азора")
        self.assertEqual(next(a), "оХ аЗОР ох АзОр Ох Азор ты влюблен подарю подарю я тебе розЫ")


if __name__ == "__main__":
    unittest.main()
