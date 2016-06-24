
"""Unit tests for a valid model to use in the Slide package.
If a model can pass all these tests, it can be used interchangeably in the program.

to test a different model implemnetation, change model0 and Model to your file and class name
"""
import unittest
import random
import slideexceptions
from model0 import Model as model


class New_Board_Tests(unittest.TestCase):
    """
    Test Cases using newly created boards
    """

    def setUp(self):
        """
        sets up common testing data
        """
        self.s_board = model(2)
        self.m_board = model(4)
        self.l_board = model(16)
        self.xl_board = model(32)

    def test_size(self):
        """
        Tests that the model has the size attribute and that said
        attribute returns the accurate size of the grid
        """
        self.run_test_size(self.s_board, 2)
        self.run_test_size(self.m_board, 4)
        self.run_test_size(self.l_board, 16)
        self.run_test_size(self.xl_board, 32)

    def run_test_size(self, m, n):
        """
        Common code for testing that the size attribute accurately
        represents the board grid represented by the model
        """
        self.assertEqual(m.size, n)
        self.assertIsNotNone(m.value_at(n - 1, n - 1))
        self.assertRaises(Exception, m.value_at, n, n)

    def test_init_boards(self):
        """
        Tests that models initialize properly
        """
        self.assertEqual(self.s_board.count_blocks(), 1)
        self.assertEqual(self.m_board.count_blocks(), 1)
        self.assertEqual(self.l_board.count_blocks(), 1)
        self.assertEqual(self.xl_board.count_blocks(), 1)

        self.assertRaises(TypeError, model, 1)
        self.assertRaises(TypeError, model, 0)
        self.assertRaises(TypeError, model, -1)
        self.assertRaises(TypeError, model, -1.3)
        self.assertRaises(TypeError, model, 0.55)
        self.assertRaises(TypeError, model, 1.55)
        self.assertRaises(TypeError, model, 2.55)

    def test_value_at(self):
        """
        Tests the value_at method of the model
        """
        self.run_test_value_at(self.s_board)
        self.run_test_value_at(self.m_board)
        self.run_test_value_at(self.l_board)
        self.run_test_value_at(self.xl_board)

    def run_test_value_at(self, m):
        """
        Common code for testing value_at
        Tests that model m retreives accurate data (an integer)
        for random valid grid coordinates
        """
        n = m.size
        self.assertIsInstance(m.value_at(int(random.random() * n), int(random.random() * n)), int)
        self.assertIsInstance(m.value_at(int(random.random() * n), int(random.random() * n)), int)
        self.assertIsInstance(m.value_at(int(random.random() * n), int(random.random() * n)), int)

    def test_add_new_block(self):
        """
        Tests the add_new_block method of the model
        """
        self.run_test_add_new_block(self.s_board, 2)
        self.run_test_add_new_block(self.m_board, 2)
        self.run_test_add_new_block(self.l_board, 2)
        self.run_test_add_new_block(self.xl_board, 2)

        self.run_test_add_new_block(self.s_board, 3)
        self.run_test_add_new_block(self.m_board, 3)
        self.run_test_add_new_block(self.l_board, 3)
        self.run_test_add_new_block(self.xl_board, 3)

        self.run_test_add_new_block(self.xl_board, 4)
        self.run_test_add_new_block(self.xl_board, 5)
        self.run_test_add_new_block(self.xl_board, 6)

        self.run_test_add_new_block(self.s_board, 4)
        self.assertRaises(slideexceptions.AddBlockError, self.run_test_add_new_block, self.s_board, 5)

    def run_test_add_new_block(self, m, n):
        """
        Common code for testing add_new_block
        Tests that m has n -1 blocks (grid squares with a value other than 0)
        in it before adding a block and n blocks after
        """
        self.assertEqual(m.count_blocks(), n - 1)
        m.add_new_block()
        self.assertEqual(m.count_blocks(), n)

    def test_add_block_at(self):
        """
        Tests add_block_at
        """
        self.run_test_add_block_at(self.s_board)
        self.run_test_add_block_at(self.m_board)
        self.run_test_add_block_at(self.l_board)
        self.run_test_add_block_at(self.xl_board)

    def run_test_add_block_at(self, m):
        """
        Common code for testing add_block_at
        """
        self.assertEqual(m.count_blocks(), 1)
        if m.value_at(0, 0) == 0:
            m.add_block_at(0, 0, 2)
        else:
            m.add_block_at(0, 1, 2)
        self.assertEqual(m.count_blocks(), 2)
        self.assertTrue(m.value_at(0, 0) or m.value_at(0, 1))


class Complex_Board_Tests(unittest.TestCase):
    """
    Test Cases using boards with complex block layouts
    """
    def setUp(self):
        """
        sets up common testing data
        """
        self.s_board = model(2)
        self.m_board = model(4)
        self.no_shift = model(2)

        self.s_board.add_block_at(0, 0, 2)
        self.s_board.add_block_at(0, 1, 2)
        self.s_board.add_block_at(1, 0, 2)
        self.s_board.add_block_at(1, 1, 2)

        self.m_board.add_block_at(0, 0, 4)
        self.m_board.add_block_at(0, 1, 2)
        self.m_board.add_block_at(0, 2, 2)
        self.m_board.add_block_at(0, 3, 2)
        self.m_board.add_block_at(1, 0, 8)
        self.m_board.add_block_at(1, 1, 2)
        self.m_board.add_block_at(1, 2, 0)
        self.m_board.add_block_at(1, 3, 0)
        self.m_board.add_block_at(2, 0, 0)
        self.m_board.add_block_at(2, 1, 2)
        self.m_board.add_block_at(2, 2, 4)
        self.m_board.add_block_at(2, 3, 0)
        self.m_board.add_block_at(3, 0, 0)
        self.m_board.add_block_at(3, 1, 0)
        self.m_board.add_block_at(3, 2, 2)
        self.m_board.add_block_at(3, 3, 4)

        self.no_shift.add_block_at(0, 0, 2)
        self.no_shift.add_block_at(1, 0, 4)
        self.no_shift.add_block_at(0, 1, 4)
        self.no_shift.add_block_at(1, 1, 2)

    def test_shift_blocks_left(self):
        """
        Tests shift_blocks_left
        """
        self.assertEqual(self.s_board.shift_blocks_left(), False)
        self.assertEqual(self.s_board.value_at(0, 0), 4)
        self.assertEqual(self.s_board.value_at(0, 1), 4)
        self.assertEqual(self.s_board.value_at(1, 0), 0)
        self.assertEqual(self.s_board.value_at(1, 1), 0)

        self.assertEqual(self.m_board.shift_blocks_left(), False)
        self.assertEqual(self.m_board.value_at(0, 0), 4)
        self.assertEqual(self.m_board.value_at(0, 1), 4)
        self.assertEqual(self.m_board.value_at(0, 2), 2)
        self.assertEqual(self.m_board.value_at(0, 3), 2)
        self.assertEqual(self.m_board.value_at(1, 0), 8)
        self.assertEqual(self.m_board.value_at(1, 1), 2)
        self.assertEqual(self.m_board.value_at(1, 2), 4)
        self.assertEqual(self.m_board.value_at(1, 3), 4)
        self.assertEqual(self.m_board.value_at(2, 0), 0)
        self.assertEqual(self.m_board.value_at(2, 1), 0)
        self.assertEqual(self.m_board.value_at(2, 2), 2)
        self.assertEqual(self.m_board.value_at(2, 3), 0)
        self.assertEqual(self.m_board.value_at(3, 0), 0)
        self.assertEqual(self.m_board.value_at(3, 1), 0)
        self.assertEqual(self.m_board.value_at(3, 2), 0)
        self.assertEqual(self.m_board.value_at(3, 3), 0)

        self.assertEqual(self.no_shift.shift_blocks_left(), True)
        self.assertEqual(self.no_shift.value_at(0, 0), 2)
        self.assertEqual(self.no_shift.value_at(1, 0), 4)
        self.assertEqual(self.no_shift.value_at(0, 1), 4)
        self.assertEqual(self.no_shift.value_at(1, 1), 2)

    def test_shift_blocks_right(self):
        """
        Tests shift_blocks_right
        """
        self.assertEqual(self.s_board.shift_blocks_right(), False)
        self.assertEqual(self.s_board.value_at(0, 0), 0)
        self.assertEqual(self.s_board.value_at(0, 1), 0)
        self.assertEqual(self.s_board.value_at(1, 0), 4)
        self.assertEqual(self.s_board.value_at(1, 1), 4)

        self.assertEqual(self.m_board.shift_blocks_right(), False)
        self.assertEqual(self.m_board.value_at(0, 0), 0)
        self.assertEqual(self.m_board.value_at(0, 1), 0)
        self.assertEqual(self.m_board.value_at(0, 2), 0)
        self.assertEqual(self.m_board.value_at(0, 3), 0)
        self.assertEqual(self.m_board.value_at(1, 0), 0)
        self.assertEqual(self.m_board.value_at(1, 1), 0)
        self.assertEqual(self.m_board.value_at(1, 2), 2)
        self.assertEqual(self.m_board.value_at(1, 3), 0)
        self.assertEqual(self.m_board.value_at(2, 0), 4)
        self.assertEqual(self.m_board.value_at(2, 1), 2)
        self.assertEqual(self.m_board.value_at(2, 2), 4)
        self.assertEqual(self.m_board.value_at(2, 3), 2)
        self.assertEqual(self.m_board.value_at(3, 0), 8)
        self.assertEqual(self.m_board.value_at(3, 1), 4)
        self.assertEqual(self.m_board.value_at(3, 2), 2)
        self.assertEqual(self.m_board.value_at(3, 3), 4)

        self.assertEqual(self.no_shift.shift_blocks_right(), True)
        self.assertEqual(self.no_shift.value_at(0, 0), 2)
        self.assertEqual(self.no_shift.value_at(1, 0), 4)
        self.assertEqual(self.no_shift.value_at(0, 1), 4)
        self.assertEqual(self.no_shift.value_at(1, 1), 2)

    def test_shift_blocks_down(self):
        """
        Tests shift_blocks_down
        """
        self.assertEqual(self.s_board.shift_blocks_down(), False)
        self.assertEqual(self.s_board.value_at(0, 0), 0)
        self.assertEqual(self.s_board.value_at(0, 1), 4)
        self.assertEqual(self.s_board.value_at(1, 0), 0)
        self.assertEqual(self.s_board.value_at(1, 1), 4)

        self.assertEqual(self.m_board.shift_blocks_down(), False)
        self.assertEqual(self.m_board.value_at(0, 0), 0)
        self.assertEqual(self.m_board.value_at(0, 1), 4)
        self.assertEqual(self.m_board.value_at(0, 2), 2)
        self.assertEqual(self.m_board.value_at(0, 3), 4)
        self.assertEqual(self.m_board.value_at(1, 0), 0)
        self.assertEqual(self.m_board.value_at(1, 1), 0)
        self.assertEqual(self.m_board.value_at(1, 2), 8)
        self.assertEqual(self.m_board.value_at(1, 3), 2)
        self.assertEqual(self.m_board.value_at(2, 0), 0)
        self.assertEqual(self.m_board.value_at(2, 1), 0)
        self.assertEqual(self.m_board.value_at(2, 2), 2)
        self.assertEqual(self.m_board.value_at(2, 3), 4)
        self.assertEqual(self.m_board.value_at(3, 0), 0)
        self.assertEqual(self.m_board.value_at(3, 1), 0)
        self.assertEqual(self.m_board.value_at(3, 2), 2)
        self.assertEqual(self.m_board.value_at(3, 3), 4)

        self.assertEqual(self.no_shift.shift_blocks_down(), True)
        self.assertEqual(self.no_shift.value_at(0, 0), 2)
        self.assertEqual(self.no_shift.value_at(1, 0), 4)
        self.assertEqual(self.no_shift.value_at(0, 1), 4)
        self.assertEqual(self.no_shift.value_at(1, 1), 2)

    def test_shift_blocks_up(self):
        """
        Tests shift_blocks_up
        """
        self.assertEqual(self.s_board.shift_blocks_up(), False)
        self.assertEqual(self.s_board.value_at(0, 0), 4)
        self.assertEqual(self.s_board.value_at(0, 1), 0)
        self.assertEqual(self.s_board.value_at(1, 0), 4)
        self.assertEqual(self.s_board.value_at(1, 1), 0)

        self.assertEqual(self.m_board.shift_blocks_up(), False)
        self.assertEqual(self.m_board.value_at(0, 0), 4)
        self.assertEqual(self.m_board.value_at(0, 1), 4)
        self.assertEqual(self.m_board.value_at(0, 2), 2)
        self.assertEqual(self.m_board.value_at(0, 3), 0)
        self.assertEqual(self.m_board.value_at(1, 0), 8)
        self.assertEqual(self.m_board.value_at(1, 1), 2)
        self.assertEqual(self.m_board.value_at(1, 2), 0)
        self.assertEqual(self.m_board.value_at(1, 3), 0)
        self.assertEqual(self.m_board.value_at(2, 0), 2)
        self.assertEqual(self.m_board.value_at(2, 1), 4)
        self.assertEqual(self.m_board.value_at(2, 2), 0)
        self.assertEqual(self.m_board.value_at(2, 3), 0)
        self.assertEqual(self.m_board.value_at(3, 0), 2)
        self.assertEqual(self.m_board.value_at(3, 1), 4)
        self.assertEqual(self.m_board.value_at(3, 2), 0)
        self.assertEqual(self.m_board.value_at(3, 3), 0)

        self.assertEquals(self.no_shift.shift_blocks_up(), True)
        self.assertEqual(self.no_shift.value_at(0, 0), 2)
        self.assertEqual(self.no_shift.value_at(1, 0), 4)
        self.assertEqual(self.no_shift.value_at(0, 1), 4)
        self.assertEqual(self.no_shift.value_at(1, 1), 2)

    def test_game_state_check(self):
        """
        Tests game_state_check
        """
        self.assertEqual(self.no_shift.game_state_check(), self.no_shift.game_states["Loss"])
        self.assertEqual(self.s_board.game_state_check(), self.s_board.game_states["Play"])
        self.assertEqual(self.m_board.game_state_check(), self.m_board.game_states["Play"])
        self.s_board.add_block_at(0, 0, self.s_board.game_goal)
        self.assertEqual(self.s_board.game_state_check(), self.s_board.game_states["Win"])

    def test_no_valid_moves(self):
        """
            Tests the method that determines if there are any valid moves on the board
        """
        self.assertTrue(self.no_shift.no_valid_moves())
        self.assertFalse(self.s_board.no_valid_moves())

suite_new = unittest.TestLoader().loadTestsFromTestCase(New_Board_Tests)
suite_complex = unittest.TestLoader().loadTestsFromTestCase(Complex_Board_Tests)
alltests = unittest.TestSuite([suite_new, suite_complex])
unittest.TextTestRunner(verbosity=2).run(alltests)
