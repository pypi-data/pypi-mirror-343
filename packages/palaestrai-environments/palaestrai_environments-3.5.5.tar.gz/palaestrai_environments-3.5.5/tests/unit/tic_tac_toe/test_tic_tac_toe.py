from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from palaestrai.agent import ActuatorInformation
from palaestrai_environments.tictactoe import TicTacToeEnvironment
from palaestrai_environments.tictactoe.tic_tac_toe_environment import Peg


class TicTacToeTest(unittest.TestCase):
    def test_start_environment_twoplayer(self):
        ttt = TicTacToeEnvironment(uid="ttt", seed=123, twoplayer=True)
        baseline = ttt.start_environment()
        self.assertTrue(all(s.value == 0 for s in baseline.sensors_available))
        self.assertEqual(len(ttt.board), 9)
        self.assertTrue(all(x == Peg.EMPTY for x in ttt.board))
        self.assertEqual(ttt._current_player, Peg.AGENT)

    def test_twoplayer(self):
        ttt = TicTacToeEnvironment(uid="ttt", seed=456, twoplayer=True)
        baseline = ttt.start_environment()
        set1 = MagicMock(sepc=baseline.actuators_available[0])
        set1.value = 1
        state = ttt.update([set1])
        set2 = MagicMock(sepc=baseline.actuators_available[0])
        set2.value = 6
        state = ttt.update([set2])
        set1.value = 2
        state = ttt.update([set1])
        set2.value = 4
        state = ttt.update([set2])
        self.assertListEqual(
            [s.value for s in state.sensor_information],
            [0, 2, 2, 0, 1, 0, 1, 0, 0],
        )


if __name__ == "__main__":
    unittest.main()
