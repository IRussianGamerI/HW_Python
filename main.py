import json


def parse_json(keyword_callback, json_str: str, required_fields=None, keywords=None):
    if required_fields is None:
        required_fields = []
    if keywords is None:
        keywords = []
    try:
        json_loaded = json.loads(json_str)
    except json.decoder.JSONDecodeError:
        raise TypeError('Given str is not JSON-like')
    for field in required_fields:
        if field in json_loaded:
            try:
                keywords_list = json_loaded[field].split(' ')
            except AttributeError:
                raise TypeError('Given value is not str')
            for value in keywords_list:
                if value in keywords:
                    keyword_callback(field, value)


def keyword_callback_example(field, key):
    print('There is a keyword "{0}" in the field "{1}"'.format(key, field))
