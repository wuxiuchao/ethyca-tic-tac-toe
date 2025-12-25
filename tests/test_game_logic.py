"""
Unit tests for Tic-Tac-Toe game logic
"""
import pytest
from app.game_logic import TicTacToeGame, GameManager


class TestTicTacToeGame:
    """Test TicTacToeGame class"""
    
    def test_game_initialization(self):
        """Test game is initialized correctly"""
        game = TicTacToeGame("test_game_1")
        assert game.game_id == "test_game_1"
        assert game.status == "in_progress"
        assert game.winner is None
        assert all(cell is None for row in game.board for cell in row)
        assert len(game.moves) == 0
        
    def test_make_valid_move(self):
        """Test making a valid move"""
        game = TicTacToeGame("test_game_1")
        result = game.make_move(0, 0, TicTacToeGame.PLAYER)
        assert result is True
        assert game.board[0][0] == 'X'
        assert len(game.moves) == 1
        assert game.moves[0]['player'] == 'player'
        assert game.moves[0]['position'] == {'row': 0, 'col': 0}
        
    def test_make_invalid_move_occupied(self):
        """Test making a move on occupied position"""
        game = TicTacToeGame("test_game_1")
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        result = game.make_move(0, 0, TicTacToeGame.SERVER)
        assert result is False
        assert game.board[0][0] == 'X'  # Should still be player's mark
        
    def test_make_invalid_move_out_of_bounds(self):
        """Test making a move out of bounds"""
        game = TicTacToeGame("test_game_1")
        assert game.make_move(3, 0, TicTacToeGame.PLAYER) is False
        assert game.make_move(0, -1, TicTacToeGame.PLAYER) is False
        assert game.make_move(5, 5, TicTacToeGame.PLAYER) is False
        
    def test_check_winner_row(self):
        """Test winning condition - row"""
        game = TicTacToeGame("test_game_1")
        # Player wins with top row
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        game.make_move(0, 1, TicTacToeGame.PLAYER)
        game.make_move(0, 2, TicTacToeGame.PLAYER)
        
        winner = game.check_winner()
        assert winner == 'player'
        
    def test_check_winner_column(self):
        """Test winning condition - column"""
        game = TicTacToeGame("test_game_1")
        # Server wins with first column
        game.make_move(0, 0, TicTacToeGame.SERVER)
        game.make_move(1, 0, TicTacToeGame.SERVER)
        game.make_move(2, 0, TicTacToeGame.SERVER)
        
        winner = game.check_winner()
        assert winner == 'server'
        
    def test_check_winner_diagonal(self):
        """Test winning condition - diagonal"""
        game = TicTacToeGame("test_game_1")
        # Player wins with diagonal
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        game.make_move(1, 1, TicTacToeGame.PLAYER)
        game.make_move(2, 2, TicTacToeGame.PLAYER)
        
        winner = game.check_winner()
        assert winner == 'player'
        
    def test_check_winner_anti_diagonal(self):
        """Test winning condition - anti-diagonal"""
        game = TicTacToeGame("test_game_1")
        # Server wins with anti-diagonal
        game.make_move(0, 2, TicTacToeGame.SERVER)
        game.make_move(1, 1, TicTacToeGame.SERVER)
        game.make_move(2, 0, TicTacToeGame.SERVER)
        
        winner = game.check_winner()
        assert winner == 'server'
        
    def test_check_draw(self):
        """Test draw condition"""
        game = TicTacToeGame("test_game_1")
        # Create a draw board:
        # X O X
        # X O O
        # O X X
        moves = [
            (0, 0, TicTacToeGame.PLAYER),  # X
            (0, 1, TicTacToeGame.SERVER),  # O
            (0, 2, TicTacToeGame.PLAYER),  # X
            (1, 0, TicTacToeGame.PLAYER),  # X
            (1, 1, TicTacToeGame.SERVER),  # O
            (1, 2, TicTacToeGame.SERVER),  # O
            (2, 0, TicTacToeGame.SERVER),  # O
            (2, 1, TicTacToeGame.PLAYER),  # X
            (2, 2, TicTacToeGame.PLAYER),  # X
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
            
        winner = game.check_winner()
        assert winner == 'draw'
        
    def test_update_status_player_wins(self):
        """Test status update when player wins"""
        game = TicTacToeGame("test_game_1")
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        game.make_move(0, 1, TicTacToeGame.PLAYER)
        game.make_move(0, 2, TicTacToeGame.PLAYER)
        
        game.update_status()
        assert game.status == 'player_wins'
        assert game.winner == 'player'
        
    def test_update_status_server_wins(self):
        """Test status update when server wins"""
        game = TicTacToeGame("test_game_1")
        game.make_move(0, 0, TicTacToeGame.SERVER)
        game.make_move(1, 1, TicTacToeGame.SERVER)
        game.make_move(2, 2, TicTacToeGame.SERVER)
        
        game.update_status()
        assert game.status == 'server_wins'
        assert game.winner == 'server'
        
    def test_update_status_draw(self):
        """Test status update for draw"""
        game = TicTacToeGame("test_game_1")
        # Create draw board
        moves = [
            (0, 0, TicTacToeGame.PLAYER),
            (0, 1, TicTacToeGame.SERVER),
            (0, 2, TicTacToeGame.PLAYER),
            (1, 0, TicTacToeGame.PLAYER),
            (1, 1, TicTacToeGame.SERVER),
            (1, 2, TicTacToeGame.SERVER),
            (2, 0, TicTacToeGame.SERVER),
            (2, 1, TicTacToeGame.PLAYER),
            (2, 2, TicTacToeGame.PLAYER),
        ]
        for row, col, player in moves:
            game.make_move(row, col, player)
            
        game.update_status()
        assert game.status == 'draw'
        assert game.winner is None
        
    def test_get_available_positions(self):
        """Test getting available positions"""
        game = TicTacToeGame("test_game_1")
        available = game.get_available_positions()
        assert len(available) == 9
        
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        available = game.get_available_positions()
        assert len(available) == 8
        assert (0, 0) not in available
        
        # Fill the board
        for row in range(3):
            for col in range(3):
                if game.board[row][col] is None:
                    game.make_move(row, col, TicTacToeGame.SERVER)
                    
        available = game.get_available_positions()
        assert len(available) == 0
        
    def test_make_random_move(self):
        """Test server making random move"""
        game = TicTacToeGame("test_game_1")
        
        move = game.make_random_move()
        assert move is not None
        row, col = move
        assert game.board[row][col] == TicTacToeGame.SERVER
        
    def test_make_random_move_no_positions(self):
        """Test random move when no positions available"""
        game = TicTacToeGame("test_game_1")
        # Fill the board
        for row in range(3):
            for col in range(3):
                game.board[row][col] = TicTacToeGame.PLAYER
                
        move = game.make_random_move()
        assert move is None
        
    def test_cannot_move_after_game_finished(self):
        """Test that moves cannot be made after game is finished"""
        game = TicTacToeGame("test_game_1")
        # Player wins
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        game.make_move(0, 1, TicTacToeGame.PLAYER)
        game.make_move(0, 2, TicTacToeGame.PLAYER)
        game.update_status()
        
        # Try to make another move
        result = game.make_move(1, 1, TicTacToeGame.SERVER)
        assert result is False
        
    def test_get_moves(self):
        """Test getting all moves"""
        game = TicTacToeGame("test_game_1")
        assert len(game.get_moves()) == 0
        
        game.make_move(0, 0, TicTacToeGame.PLAYER)
        game.make_move(1, 1, TicTacToeGame.SERVER)
        
        moves = game.get_moves()
        assert len(moves) == 2
        assert moves[0]['player'] == 'player'
        assert moves[1]['player'] == 'server'
        
    def test_to_dict(self):
        """Test converting game to dictionary"""
        game = TicTacToeGame("test_game_1")
        game_dict = game.to_dict()
        
        assert game_dict['game_id'] == "test_game_1"
        assert game_dict['status'] == 'in_progress'
        assert game_dict['winner'] is None
        assert 'board' in game_dict
        assert 'created_at' in game_dict


class TestGameManager:
    """Test GameManager class"""
    
    def test_create_game(self):
        """Test creating a new game"""
        manager = GameManager()
        game = manager.create_game()
        
        assert game is not None
        assert game.game_id == "game_1"
        assert game.status == "in_progress"
        
    def test_create_multiple_games(self):
        """Test creating multiple games"""
        manager = GameManager()
        game1 = manager.create_game()
        game2 = manager.create_game()
        game3 = manager.create_game()
        
        assert game1.game_id == "game_1"
        assert game2.game_id == "game_2"
        assert game3.game_id == "game_3"
        assert len(manager.games) == 3
        
    def test_get_game(self):
        """Test getting a game by ID"""
        manager = GameManager()
        game = manager.create_game()
        
        retrieved_game = manager.get_game(game.game_id)
        assert retrieved_game is game
        
    def test_get_nonexistent_game(self):
        """Test getting a game that doesn't exist"""
        manager = GameManager()
        game = manager.get_game("nonexistent")
        assert game is None
        
    def test_get_all_games_chronological(self):
        """Test getting all games in chronological order"""
        manager = GameManager()
        game1 = manager.create_game()
        game2 = manager.create_game()
        game3 = manager.create_game()
        
        all_games = manager.get_all_games()
        assert len(all_games) == 3
        assert all_games[0] is game1
        assert all_games[1] is game2
        assert all_games[2] is game3
        
    def test_get_all_games_empty(self):
        """Test getting all games when there are none"""
        manager = GameManager()
        all_games = manager.get_all_games()
        assert len(all_games) == 0

