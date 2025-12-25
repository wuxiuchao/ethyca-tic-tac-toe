"""
Tic-Tac-Toe game logic implementation
"""
import random
from typing import List, Optional, Tuple, Dict
from datetime import datetime


class TicTacToeGame:
    """Represents a single tic-tac-toe game"""
    
    PLAYER = 'X'
    SERVER = 'O'
    EMPTY = None
    
    def __init__(self, game_id: str):
        self.game_id = game_id
        self.board: List[List[Optional[str]]] = [[None, None, None] for _ in range(3)]
        self.moves: List[dict] = []
        self.status = 'in_progress'
        self.winner: Optional[str] = None
        self.created_at = datetime.utcnow()
        
    def make_move(self, row: int, col: int, player: str) -> bool:
        """
        Make a move on the board
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            player: 'X' for player or 'O' for server
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self._is_valid_move(row, col):
            return False
            
        self.board[row][col] = player
        self.moves.append({
            'player': 'player' if player == self.PLAYER else 'server',
            'position': {'row': row, 'col': col},
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        })
        
        return True
        
    def _is_valid_move(self, row: int, col: int) -> bool:
        """Check if a move is valid"""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        if self.board[row][col] is not None:
            return False
        if self.status != 'in_progress':
            return False
        return True
        
    def check_winner(self) -> Optional[str]:
        """
        Check if there's a winner
        
        Returns:
            'player' if player wins, 'server' if server wins, 'draw' if it's a draw, None if game continues
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return 'player' if row[0] == self.PLAYER else 'server'
                
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return 'player' if self.board[0][col] == self.PLAYER else 'server'
                
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return 'player' if self.board[0][0] == self.PLAYER else 'server'
            
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return 'player' if self.board[0][2] == self.PLAYER else 'server'
            
        # Check for draw
        if all(self.board[row][col] is not None for row in range(3) for col in range(3)):
            return 'draw'
            
        return None
        
    def update_status(self):
        """Update game status based on current board state"""
        result = self.check_winner()
        if result == 'player':
            self.status = 'player_wins'
            self.winner = 'player'
        elif result == 'server':
            self.status = 'server_wins'
            self.winner = 'server'
        elif result == 'draw':
            self.status = 'draw'
            self.winner = None
        else:
            self.status = 'in_progress'
            
    def get_available_positions(self) -> List[Tuple[int, int]]:
        """Get list of available positions"""
        positions = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    positions.append((row, col))
        return positions
        
    def make_random_move(self) -> Optional[Tuple[int, int]]:
        """
        Server makes a random move
        
        Returns:
            Tuple of (row, col) if move was made, None if no moves available
        """
        available = self.get_available_positions()
        if not available:
            return None
            
        row, col = random.choice(available)
        self.make_move(row, col, self.SERVER)
        return (row, col)
        
    def to_dict(self) -> dict:
        """Convert game to dictionary representation"""
        return {
            'game_id': self.game_id,
            'board': self.board,
            'status': self.status,
            'winner': self.winner,
            'created_at': self.created_at.isoformat() + 'Z'
        }
        
    def get_moves(self) -> List[dict]:
        """Get all moves in chronological order"""
        return self.moves.copy()


class GameManager:
    """Manages multiple games"""
    
    def __init__(self):
        self.games: Dict[str, TicTacToeGame] = {}
        self.game_counter = 0
        
    def create_game(self) -> TicTacToeGame:
        """Create a new game"""
        self.game_counter += 1
        game_id = f"game_{self.game_counter}"
        game = TicTacToeGame(game_id)
        self.games[game_id] = game
        return game
        
    def get_game(self, game_id: str) -> Optional[TicTacToeGame]:
        """Get a game by ID"""
        return self.games.get(game_id)
        
    def get_all_games(self) -> List[TicTacToeGame]:
        """Get all games in chronological order"""
        return sorted(self.games.values(), key=lambda g: g.created_at)

