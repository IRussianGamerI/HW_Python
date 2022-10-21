class LRUCache:

    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError("limit must be int")
        if limit <= 0:
            raise ValueError("limit must be positive")
        self.data = {}
        self.limit = limit

    def get(self, key):
        if key not in self.data.keys():
            return None
        value = self.data.pop(key)
        self.data[key] = value
        return value

    def set(self, key, value):
        if key in self.data.keys():
            self.data.pop(key)
        elif len(self.data.keys()) == self.limit:
            self.data.pop(list(self.data.keys())[0])
        self.data[key] = value
