import cProfile
import io
import pstats


def profile_deco(func):
    class Wrapper:
        def __init__(self):
            self.profiler = cProfile.Profile()

        def __call__(self, *args, **kwargs):
            self.profiler.enable()
            result = func(*args, **kwargs)
            self.profiler.disable()
            return result

        def print_stat(self):
            out = io.StringIO()
            stats = pstats.Stats(self.profiler, stream=out).sort_stats("cumulative")
            stats.print_stats()

            print(out.getvalue())

    return Wrapper()


@profile_deco
def add(lhs, rhs):
    return lhs + rhs


@profile_deco
def sub(lhs, rhs):
    return lhs - rhs


def mul(lhs, rhs):
    return lhs * rhs


@profile_deco
def func_with_secrets_inside(lhs, rhs):
    print("Called function with inner call")
    return mul(lhs, rhs)


if __name__ == "__main__":
    # Демонстрация пополнения статистики вызовов
    for _ in range(1_000_000):
        add(10, 20)

    add.print_stat()

    for _ in range(1_000_000):
        sub(20, 10)

    sub.print_stat()

    for _ in range(1_000):
        add(10, 20)

    add.print_stat()

    for _ in range(1_000):
        sub(20, 10)

    sub.print_stat()

    # Вызов сложной функции
    func_with_secrets_inside(20, 10)

    func_with_secrets_inside.print_stat()
