import time
import weakref


class Dict(dict):
    pass


class List(list):
    pass


class MyPreciousClass:
    def __init__(self):
        self.str_attr = f"My precious class to be tested"
        self.list_attr = List(self.str_attr.split())
        self.dict_attr = Dict({word: number for number, word in enumerate(self.list_attr)})


class MyPreciousClassWithSlots:
    __slots__ = ("dict_attr", "str_attr", "list_attr")

    def __init__(self):
        self.str_attr = f"My precious class to be tested"
        self.list_attr = List(self.str_attr.split())
        self.dict_attr = Dict({word: number for number, word in enumerate(self.list_attr)})


LIST_INSTANCE = List(["My", "precious", "class", "to", "be", "tested"])
DICT_INSTANCE = Dict({word: number for number, word in enumerate(LIST_INSTANCE)})


class MyPreciousClassWithWeakrefs:
    def __init__(self):
        self.str_attr = f"My precious class to be tested"
        self.list_attr = weakref.ref(LIST_INSTANCE)
        self.dict_attr = weakref.ref(DICT_INSTANCE)


def process_attrs_in_list(lst):
    for instance in lst:
        instance.int_attr += 1
        instance.str_attr += " processed"
        instance.list_attr.append("processed")


N = 1_000_000

if __name__ == "__main__":
    print("ТЕСТ СОЗДАНИЯ ПАЧКИ ЭЛЕМЕНТОВ\n")

    mpc_time_start = time.time()
    my_precious_list = [MyPreciousClass() for _ in range(N)]
    mpc_time_end = time.time()

    print(f"{N} обычных экземпляров создались за {mpc_time_end - mpc_time_start} с")

    mpc_ws_time_start = time.time()
    my_precious_list_with_slots = [MyPreciousClassWithSlots() for _ in range(N)]
    mpc_ws_time_end = time.time()

    print(f"{N} экземпляров со слотами создались за {mpc_ws_time_end - mpc_ws_time_start} с")

    mpc_weakrefs_time_start = time.time()
    my_precious_list_with_weakrefs = [MyPreciousClassWithWeakrefs() for _ in range(N)]
    mpc_weakrefs_time_end = time.time()

    print(f"{N} экземпляров с weakref'ами создались за {mpc_weakrefs_time_end - mpc_weakrefs_time_start} с")
