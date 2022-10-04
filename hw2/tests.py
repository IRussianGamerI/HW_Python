import main
import unittest
from unittest.mock import patch
import json
import random
from faker import Faker


def counter(document: dict, fields, values):
    count = 0
    for field in fields:
        for value in document[field]:
            if value in values:
                count += 1
    return count


def generate_fake_json():
    fake = Faker(locale="Ru_ru")
    fake_doc = {}
    field_set = set()
    for i in range(random.randint(3, 10)):
        field = str(fake.country())
        while field in field_set:
            field = str(fake.country())
        cur_value_list = []
        for j in range(random.randint(3, 10)):
            cur_value_list.append(fake.last_name())
        fake_doc[field] = ' '.join(cur_value_list)
        field_set.add(field)
    fake_json = json.dumps(fake_doc)
    return fake_json, fake_doc


def generate_arguments(document: dict):
    for field in document:
        document[field] = document[field].split(' ')
    nb_field = random.randint(1, len(document.keys()))
    required_field = random.sample(list(document), nb_field)
    required_value = []
    for field in required_field:
        cur_nb_val = random.randint(1, len(document[field]))
        required_value.extend(random.sample(document[field], cur_nb_val))
    count = counter(document, required_field, required_value)
    return required_field, required_value, count


class JsonParserTest(unittest.TestCase):

    @patch('main.keyword_callback_example')
    def test_keywords_callback_count(self, mocker):
        fake_json, fake_doc = generate_fake_json()
        required_fields, keywords, count = generate_arguments(fake_doc)
        main.parse_json(mocker, fake_json, required_fields, keywords)
        self.assertEqual(mocker.call_count, count)

    def test_exceptions(self):
        json_str = '{99.99: "Alpha lupi", "key2": "Fragile piccolo"}'
        with self.assertRaises(TypeError):
            main.parse_json(main.keyword_callback_example, json_str, ['key1'], ['lupi'])
        json_str = '{"Savathun": "Witch queen", "Article": 228}'
        with self.assertRaises(TypeError):
            main.parse_json(main.keyword_callback_example, json_str, ['Article'], ['228'])

    def test_success(self):
        try:
            json_str = '{"BMSTU": "University", "HSE": "Sharaga"}'
            main.parse_json(main.keyword_callback_example, json_str, ['BMSTU'], ['University'])
        except TypeError:
            self.assertEqual(0, 1)
        else:
            self.assertEqual(1, 1)

    @patch('main.keyword_callback_example')
    def test_none(self, mocker):
        fake_json, fake_doc = generate_fake_json()
        required_fields, keywords, count = None, None, 0
        main.parse_json(mocker, fake_json, required_fields, keywords)
        self.assertEqual(mocker.call_count, count)


if __name__ == '__main__':
    unittest.main()
