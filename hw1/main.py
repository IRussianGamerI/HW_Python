class TicTacGame:

    def __init__(self, __cells=None):  # For testing only
        if __cells is not None:
            self.cells = __cells
        else:
            self.cells = list(range(1, 10))

    def show_board(self):
        for i in range(0, 7, 3):
            print('', self.cells[i], '│', self.cells[i + 1],
                  '│', self.cells[i + 2])
            if i < 6:
                print("───┼───┼───")

    def validate_input(self, cell):
        try:
            cell = int(cell)
        except ValueError as exc:
            raise TypeError("Необходимо ввести целое число") from exc  # Получили на вход не число
            # => ошибка типа
        else:
            if 1 <= cell <= 9:
                return str(self.cells[cell - 1]) not in "XO"
            raise IndexError("Вводимое число должно лежать в диапазоне [1, 9]")

    def start_game(self):
        print("Игра началась!")
        win_check = False
        steps_num = 0
        self.show_board()
        while not win_check:
            validation = True
            while validation:
                sym = "O" if steps_num % 2 else "X"
                cell = input("Куда вы хотите поставить " + sym + "? ")
                try:
                    check_input = self.validate_input(cell)
                except TypeError as type_err:
                    print(type_err.args[0])
                except IndexError as ind_err:
                    print(ind_err.args[0])

                else:
                    if check_input:
                        self.cells[int(cell) - 1] = sym
                        validation = False
                        self.show_board()
                    else:
                        print("Клетка занята! В ней уже стоит " + self.cells[int(cell) - 1] + "!")

            steps_num += 1
            if steps_num >= 5:
                win_check = self.check_winner()
                if win_check:
                    print(f"Победил игрок {win_check}!")
                    break
            if steps_num == 9:
                self.show_board()
                print("Ничья!")
                break

        return win_check

    def check_winner(self):
        combs = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                 (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for i in combs:
            if self.cells[i[0]] == self.cells[i[1]] == self.cells[i[2]]:
                return 1 if self.cells[i[0]] == "X" else 2
        return 0


if __name__ == "__main__":
    game = TicTacGame()
    game.start_game()
