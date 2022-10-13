class CustomMeta(type):
    @staticmethod
    def __is_magic_attr(name):
        return name.startswith("__") and name.endswith("__")

    def __init__(cls, name, bases, classdict, **kwargs):
        super().__init__(name, bases, classdict, **kwargs)

    def __new__(mcs, name, bases, classdict, **kwargs):
        new_classdict = {}
        for key in classdict:
            if CustomMeta.__is_magic_attr(key):
                new_classdict[key] = classdict[key]
            else:
                new_classdict['custom_' + key] = classdict[key]

        def change_name(self, _name, value):
            _name = "custom_" + _name if not mcs.__is_magic_attr(_name) else _name
            object.__setattr__(self, _name, value)

        new_classdict['__setattr__'] = change_name
        return super().__new__(mcs, name, bases, new_classdict, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)
