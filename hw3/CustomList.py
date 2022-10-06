class CustomList(list):
    def sum(self):
        return sum(self)

    def __eq__(self, other):
        return self.sum() == other.sum()

    def __ne__(self, other):
        return self.sum() != other.sum()

    def __lt__(self, other):
        return self.sum() < other.sum()

    def __le__(self, other):
        return self.sum() <= other.sum()

    def __gt__(self, other):
        return self.sum() > other.sum()

    def __ge__(self, other):
        return self.sum() >= other.sum()

    def __str__(self):
        return super().__str__() + ' ' + str(self.sum())

    def __add__(self, other):
        if len(self) >= len(other):
            addition_result = CustomList(self)
            for i, elem in enumerate(other):
                addition_result[i] += elem
        else:
            addition_result = CustomList(other)
            for i, elem in enumerate(self):
                addition_result[i] += elem

        return addition_result

    def __sub__(self, other):
        return self.__add__(CustomList(map(lambda x: -x, other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return CustomList(map(lambda x: -x, self.__sub__(other)))
