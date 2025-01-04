# test-tarkista_voittaja.py
import unittest
import Game

class TestTarkistaVoittaja(unittest.TestCase):
    
    def test_tie(self):
        # Arrange
        player_move = "Rock"
        #computer_move = "Rock"
        computer_move = "Scissors"
        # Act
        receive = Game.tarkista_voittaja(player_move,computer_move)
        # Assert
        self.assertEqual(receive, "tie")
        
    def test_player_wins(self):
        # Arrange
        player_move = "Rock"
        #computer_move = "Scissors"
        computer_move = "Rock"
        # Act
        receive = Game.tarkista_voittaja(player_move,computer_move)
        # Assert
        self.assertEqual(receive, "player")
        
    def test_computer_wins(self):
        # Arrange
        player_move = "Rock"
        #computer_move = "Paper"
        computer_move = "Rock"
        # Act
        receive = Game.tarkista_voittaja(player_move,computer_move)
        # Assert
        self.assertEqual(receive, "computer")

if __name__ == "__main__":
    unittest.main()
