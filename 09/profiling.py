import cProfile
import io
from memory_profiler import profile
import pstats

from classes import MyPreciousClass, \
    MyPreciousClassWithSlots, \
    MyPreciousClassWithWeakrefs, \
    StrWrap, \
    Dict, \
    List, \
    process_attrs_in_list, \
    process_weakrefs_in_list

N = 1_000_000


@profile
def to_be_profiled():
    pr = cProfile.Profile()
    pr.enable()

    my_precious_list = [MyPreciousClass() for _ in range(N)]
    my_precious_list_with_slots = [MyPreciousClassWithSlots() for _ in range(N)]
    my_precious_list_with_weakrefs = [MyPreciousClassWithWeakrefs() for _ in range(N)]

    process_attrs_in_list(my_precious_list)
    process_attrs_in_list(my_precious_list_with_slots)
    process_weakrefs_in_list(my_precious_list_with_weakrefs)

    pr.disable()

    out = io.StringIO()
    ps = pstats.Stats(pr, stream=out)
    ps.print_stats()

    print(out.getvalue())


if __name__ == "__main__":
    to_be_profiled()
