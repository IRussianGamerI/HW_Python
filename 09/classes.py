import time
import weakref


class Dict(dict):
    pass


class List(list):
    pass


class StrWrap:
    def __init__(self, str_val):
        self.value = str_val


class MyPreciousClass:
    def __init__(self):
        self.str_attr = StrWrap("My precious class to be tested")
        self.list_attr = List(self.str_attr.value.split())
        self.dict_attr = Dict(
            {word: number for number, word in enumerate(self.list_attr)}
        )


class MyPreciousClassWithSlots:
    __slots__ = ("dict_attr", "str_attr", "list_attr")

    def __init__(self):
        self.str_attr = StrWrap("My precious class to be tested")
        self.list_attr = List(self.str_attr.value.split())
        self.dict_attr = Dict(
            {word: number for number, word in enumerate(self.list_attr)}
        )


STR_WRAP_INSTANCE = StrWrap("My precious class to be tested")
LIST_INSTANCE = List(["My", "precious", "class", "to", "be", "tested"])
DICT_INSTANCE = Dict({word: number for number, word in enumerate(LIST_INSTANCE)})


class MyPreciousClassWithWeakrefs:
    def __init__(self):
        self.str_attr = weakref.ref(STR_WRAP_INSTANCE)
        self.list_attr = weakref.ref(LIST_INSTANCE)
        self.dict_attr = weakref.ref(DICT_INSTANCE)


def process_attrs_in_list(lst):
    for instance in lst:
        instance.dict_attr["deleted"] = instance.list_attr[0] + " str_attr"
        delattr(instance, "str_attr")
        instance.list_attr.append("processed")


def process_weakrefs_in_list(lst):
    for item in lst:
        delattr(item, "str_attr")
    if len(lst):
        lst[0].dict_attr()["deleted"] = lst[0].list_attr()[0] + " str_attr"
        lst[0].list_attr().append("processed")


N = 1_000_000

if __name__ == "__main__":
    print("ИЗМЕРЕНИЕ ВРЕМЕНИ СОЗДАНИЯ ПАЧКИ ЭКЗЕМПЛЯРОВ\n")

    mpc_time_start = time.time()
    my_precious_list = [MyPreciousClass() for _ in range(N)]
    mpc_time_end = time.time()

    print(f"{N} обычных экземпляров создались за {mpc_time_end - mpc_time_start} с")

    mpc_ws_time_start = time.time()
    my_precious_list_with_slots = [MyPreciousClassWithSlots() for _ in range(N)]
    mpc_ws_time_end = time.time()

    print(
        f"{N} экземпляров со слотами создались за {mpc_ws_time_end - mpc_ws_time_start} с"
    )

    mpc_weakrefs_time_start = time.time()
    my_precious_list_with_weakrefs = [MyPreciousClassWithWeakrefs() for _ in range(N)]
    mpc_weakrefs_time_end = time.time()

    print(
        f"{N} экземпляров с weakref'ами создались за {mpc_weakrefs_time_end - mpc_weakrefs_time_start} с"
    )

    print("\nИЗМЕРЕНИЕ ВРЕМЕНИ ДОСТУПА/ИМЕНЕНИЯ/УДАЛЕНИЯ АТРИБУТОВ\n")

    mod_start = time.time()
    process_attrs_in_list(my_precious_list)
    mod_end = time.time()

    print(f"Время обработки {N} обычных экземпляров составило {mod_end - mod_start} с")

    mod_slots_start = time.time()
    process_attrs_in_list(my_precious_list_with_slots)
    mod_slots_end = time.time()

    print(
        f"Время обработки {N} экземпляров со слотами составило {mod_slots_end - mod_slots_start} с"
    )

    mod_weakrefs_start = time.time()
    process_weakrefs_in_list(my_precious_list_with_weakrefs)
    mod_weakrefs_end = time.time()

    print(
        f"Время обработки {N} экземпляров с weakref'ами составило {mod_weakrefs_end - mod_weakrefs_start} с"
    )
