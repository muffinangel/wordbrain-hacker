"""Unit test for solver.py"""

import solver
import unittest

class KnownValues(unittest.TestCase):
    known_values = (
        (   [['b', 'a', 's'],
		     ['ó', 's', 'z'],
			 ['l', 'a', 'n']
		    ],
        [3, 6],
        [[('ból', ((0, 0), (1, 0), (2, 0))), ('szansa', (  (0, 2), (1, 2), (2, 1), (2, 2), (1, 1), (0, 1)  )  ) ]] ),

       (   [['n', 'r', 'k'],
			['u', 'a', 't'],
			['m', 'e', 'f']
		   ],
        [4, 5],
        [ [('naft', ((0, 0), (1, 1), (2, 2), (1, 2))), ('murek', ((2, 0), (1, 0), (1, 1), (2, 1), (2, 2)))],
          [('fakt', ((2, 2), (1, 1), (0, 2), (1, 2))), ('numer', ((0, 0), (1, 0), (2, 0), (2, 1), (1, 1)))] ] ),
        (  [['d', 'r', 'k'],
			['ó', 'o', 'k'],
			['w', 'o', 'p']
		],
        [5, 4],
        [ [('powód', ((2, 2), (1, 1), (2, 0), (1, 0), (0, 0))), ('krok', ((1, 2), (1, 1), (2, 1), (2, 2)))],
          [('powód', ((2, 2), (1, 1), (2, 0), (1, 0), (0, 0))), ('krok', ((2, 2), (1, 1), (2, 1), (1, 2)))],
          [('powód', ((2, 2), (2, 1), (2, 0), (1, 0), (0, 0))), ('krok', ((1, 2), (1, 1), (2, 1), (2, 2)))],
          [('powód', ((2, 2), (2, 1), (2, 0), (1, 0), (0, 0))), ('krok', ((2, 2), (1, 1), (2, 1), (1, 2)))] ]
        )

    )

    def test_solving_board_values(self):
        for board, numbers, words in self.known_values:
            solutions = []
            solver.solve_board(board, numbers, solutions)
            self.assertEqual(words, solutions)

class KnownRemovings(unittest.TestCase):
    known_values = (
        (   [['x', 'x', 'x'],
			['x', 'x', 'x'],
			['x', 'x', 'x']
            ],
            ((0,0), (1,1), (2,2)),
            [[' ', ' ', ' '],
			['x', 'x', 'x'],
			['x', 'x', 'x']
            ],
        ),
        (   [[' ', ' ', ' '],
			['x', 'x', ' '],
			[' ', ' ', ' ']
            ],
            ( (1,1), ),
            [[' ', ' ', ' '],
			[' ', ' ', ' '],
			['x', ' ', ' ']
            ],
        )
    )

    def test_removing_from_board(self):
        for board, indexes, new_board in self.known_values:
            result = solver.remove_from_board(board, indexes)
            self.assertEqual(new_board, result)

if __name__ == "__main__":
    unittest.main()
