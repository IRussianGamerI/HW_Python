import unittest
from main import TicTacGame


class TicTacGameTests(unittest.TestCase):

    def test_check_winner_1(self):
        self.assertEqual(TicTacGame(['X', 'X', 'X', 4, 'O', 'O', 7, 8, 9]).check_winner(), 1)

    def test_check_winner_2(self):
        self.assertEqual(TicTacGame([1, 2, 3, 'X', 'X', 'X', 'O', 'O', 9]).check_winner(), 1)

    def test_check_winner_3(self):
        self.assertEqual(TicTacGame([1, 2, 3,
                                     4, 'O', 'O',
                                     'X', 'X', 'X']).check_winner(), 1)

    def test_check_winner_4(self):
        self.assertEqual(TicTacGame(['X', 2, 'O',
                                     4, 'X', 'O',
                                     7, 8, 'X']).check_winner(), 1)

    def test_check_winner_5(self):
        self.assertEqual(TicTacGame(['O', 'O', 'X',
                                     4, 'X', 6,
                                     'X', 8, 9]).check_winner(), 1)

    def test_check_winner_6(self):
        self.assertEqual(TicTacGame(['O', 'O', 'O',
                                     4, 'X', 6,
                                     'X', 8, 9]).check_winner(), 2)

    def test_check_winner_7(self):
        self.assertEqual(TicTacGame(['X', 2, 'X',
                                     'O', 'O', 'O',
                                     'O', 8, 'X']).check_winner(), 2)

    def test_check_winner_8(self):
        self.assertEqual(TicTacGame(['X', 2, 'X',
                                     4, 'X', 6,
                                     'O', 'O', 'O']).check_winner(), 2)

    def test_check_winner_9(self):
        self.assertEqual(TicTacGame(['O', 2, 'X',
                                     4, 'O', 'X',
                                     'X', 8, 'O']).check_winner(), 2)

    def test_check_winner_10(self):
        self.assertEqual(TicTacGame(['X', 'X', 'O',
                                     'X', 'O', 6,
                                     'O', 8, 9]).check_winner(), 2)

    def test_check_winner_11(self):
        self.assertEqual(TicTacGame(['X', 'O', 'X',
                                     'O', 'O', 'X',
                                     'X', 'X', 'O']).check_winner(), 0)

    def test_validate_input_1(self):
        instance = None
        try:
            TicTacGame().validate_input('qwerty')
        except TypeError as t_err:
            instance = t_err
        finally:
            self.assertTrue(isinstance(instance, TypeError))

    def test_validate_input_2(self):
        instance = None
        try:
            TicTacGame().validate_input('228')
        except IndexError as ind_err:
            instance = ind_err
        finally:
            self.assertTrue(isinstance(instance, IndexError))

    def test_validate_input_3(self):
        instance = None
        try:
            TicTacGame().validate_input('228.2')
        except TypeError as t_err:
            instance = t_err
        finally:
            self.assertTrue(isinstance(instance, TypeError))

    def test_validate_input_4(self):
        instance = None
        try:
            TicTacGame().validate_input('228+322-501ю*Technopark@VKxМГТУ')
        except TypeError as t_err:
            instance = t_err
        finally:
            self.assertTrue(isinstance(instance, TypeError))

    def test_validate_input_5(self):
        self.assertTrue(TicTacGame().validate_input('4'))

    def test_validate_input_6(self):
        self.assertFalse(TicTacGame(['X', 'X', 'O',
                                     'X', 'O', 6,
                                     'O', 8, 9]).validate_input('4'))


if __name__ == '__main__':
    unittest.main()
