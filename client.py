#!/usr/bin/env python3
"""
CLI client for Tic-Tac-Toe game
"""
import sys
import requests
import json
from typing import Optional


class TicTacToeClient:
    """Client for interacting with Tic-Tac-Toe server"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.current_game_id: Optional[str] = None
        
    def create_game(self) -> bool:
        """Create a new game"""
        try:
            response = requests.post(f"{self.base_url}/game")
            if response.status_code == 201:
                data = response.json()
                self.current_game_id = data['game_id']
                print(f"\n✓ New game created: {self.current_game_id}")
                print(data.get('message', ''))
                self._display_board(data['board'])
                return True
            else:
                print(f"✗ Error creating game: {response.json().get('error', 'Unknown error')}")
                return False
        except requests.RequestException as e:
            print(f"✗ Connection error: {e}")
            print("Make sure the server is running on", self.base_url)
            return False
            
    def make_move(self, row: int, col: int) -> bool:
        """Make a move at specified position"""
        if not self.current_game_id:
            print("✗ No active game. Create a new game first.")
            return False
            
        try:
            response = requests.post(
                f"{self.base_url}/game/{self.current_game_id}/move",
                json={'row': row, 'col': col}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✓ Move made at ({row}, {col})")
                self._display_board(data['board'])
                print(f"Status: {data['status']}")
                
                if data.get('winner'):
                    print(f"Winner: {data['winner']}")
                    
                print(data.get('message', ''))
                
                # If game is over, clear current game
                if data['status'] != 'in_progress':
                    print(f"\nGame {self.current_game_id} has ended.")
                    self.current_game_id = None
                    
                return True
            else:
                error_data = response.json()
                print(f"✗ Error: {error_data.get('error', 'Unknown error')}")
                if 'details' in error_data:
                    print(f"  Details: {error_data['details']}")
                return False
                
        except requests.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
            
    def get_moves(self, game_id: Optional[str] = None) -> bool:
        """Get all moves for a game"""
        if game_id is None:
            game_id = self.current_game_id
            
        if not game_id:
            print("✗ No game ID specified and no active game.")
            return False
            
        try:
            response = requests.get(f"{self.base_url}/game/{game_id}/moves")
            
            if response.status_code == 200:
                data = response.json()
                moves = data['moves']
                
                print(f"\n=== Moves for game {game_id} ===")
                if not moves:
                    print("No moves yet.")
                else:
                    for i, move in enumerate(moves, 1):
                        player = move['player']
                        pos = move['position']
                        timestamp = move['timestamp']
                        print(f"{i}. {player.upper()} -> ({pos['row']}, {pos['col']}) at {timestamp}")
                        
                return True
            else:
                print(f"✗ Error: {response.json().get('error', 'Unknown error')}")
                return False
                
        except requests.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
            
    def list_games(self) -> bool:
        """List all games"""
        try:
            response = requests.get(f"{self.base_url}/games")
            
            if response.status_code == 200:
                data = response.json()
                games = data['games']
                
                print(f"\n=== All Games ({len(games)} total) ===")
                if not games:
                    print("No games yet.")
                else:
                    for game in games:
                        game_id = game['game_id']
                        status = game['status']
                        winner = game.get('winner', 'N/A')
                        created_at = game['created_at']
                        
                        print(f"\nGame ID: {game_id}")
                        print(f"  Status: {status}")
                        print(f"  Winner: {winner}")
                        print(f"  Created: {created_at}")
                        print(f"  Final board:")
                        self._display_board(game['board'], indent=4)
                        
                return True
            else:
                print(f"✗ Error: {response.json().get('error', 'Unknown error')}")
                return False
                
        except requests.RequestException as e:
            print(f"✗ Connection error: {e}")
            return False
            
    def _display_board(self, board, indent=0):
        """Display the game board"""
        indent_str = ' ' * indent
        print(f"{indent_str}     0   1   2")
        print(f"{indent_str}   +---+---+---+")
        for i, row in enumerate(board):
            cells = [cell if cell else ' ' for cell in row]
            print(f"{indent_str} {i} | {cells[0]} | {cells[1]} | {cells[2]} |")
            print(f"{indent_str}   +---+---+---+")
            
    def print_help(self):
        """Print help message"""
        help_text = """
=== Tic-Tac-Toe CLI Client ===

Commands:
  new                     - Create a new game
  move <row> <col>        - Make a move at position (row, col). Row and col are 0-2.
  moves [game_id]         - Show all moves for current or specified game
  list                    - List all games
  help                    - Show this help message
  quit / exit             - Exit the client

Examples:
  > new                   # Start a new game
  > move 0 0              # Place your mark at top-left corner
  > move 1 1              # Place your mark at center
  > moves                 # Show all moves in current game
  > list                  # List all games
  > quit                  # Exit

Notes:
  - You are 'X' and the server is 'O'
  - The server will automatically make its move after yours
  - Board positions are (row, col) with indices 0-2
"""
        print(help_text)
        
    def run(self):
        """Run the interactive CLI"""
        print("=== Tic-Tac-Toe CLI Client ===")
        print(f"Connecting to server at {self.base_url}")
        print("Type 'help' for available commands\n")
        
        while True:
            try:
                command = input("> ").strip().lower()
                
                if not command:
                    continue
                    
                parts = command.split()
                cmd = parts[0]
                
                if cmd in ['quit', 'exit']:
                    print("Goodbye!")
                    break
                    
                elif cmd == 'help':
                    self.print_help()
                    
                elif cmd == 'new':
                    self.create_game()
                    
                elif cmd == 'move':
                    if len(parts) != 3:
                        print("✗ Usage: move <row> <col>")
                        continue
                    try:
                        row = int(parts[1])
                        col = int(parts[2])
                        self.make_move(row, col)
                    except ValueError:
                        print("✗ Row and col must be integers")
                        
                elif cmd == 'moves':
                    game_id = parts[1] if len(parts) > 1 else None
                    self.get_moves(game_id)
                    
                elif cmd == 'list':
                    self.list_games()
                    
                else:
                    print(f"✗ Unknown command: {cmd}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"✗ Error: {e}")


def main():
    """Main entry point"""
    # Parse command line arguments for custom server URL
    base_url = "http://localhost:5000"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
        
    client = TicTacToeClient(base_url)
    client.run()


if __name__ == '__main__':
    main()

