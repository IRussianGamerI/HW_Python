import unittest
from io import StringIO

from filter_file import filter_file


class TestFilterFile(unittest.TestCase):
    def test_exception(self):
        with self.assertRaises(TypeError):
            gen = filter_file(19, ["Тык-тык"])
            next(gen)
        with self.assertRaises(TypeError):
            gen = filter_file("filename", "word")
            next(gen)
        with self.assertRaises(ValueError):
            gen = filter_file("filename", ["word1", "word2", 1337])
            next(gen)
        with self.assertRaises(ValueError):
            with open("test_file", "a", encoding="utf-8") as file:
                gen = filter_file(file, ["correct", "list"])
                next(gen)

    def test_file_object(self):
        file = StringIO(
            """Блах блах блах лютик Корусант розмарин
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
А азорУ"""
        )
        gen = filter_file(file, ["РозА", "азоР"])
        self.assertEqual(next(gen), "Роза")
        self.assertEqual(next(gen), "Азор")
        self.assertEqual(next(gen), "а Роза упала на лапу Азора")
        self.assertEqual(
            next(gen), "оХ аЗОР ох АзОр Ох Азор ты влюблен подарю подарю я тебе розЫ"
        )

    def test_filename(self):
        gen = filter_file("test_file", ["РозА", "азоР"])
        self.assertEqual(next(gen), "Роза")
        self.assertEqual(next(gen), "Азор")
        self.assertEqual(next(gen), "а Роза упала на лапу Азора")
        self.assertEqual(
            next(gen), "оХ аЗОР ох АзОр Ох Азор ты влюблен подарю подарю я тебе розЫ"
        )


if __name__ == "__main__":
    unittest.main()
