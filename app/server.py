"""
Flask server implementation for Tic-Tac-Toe game
"""
import logging
import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from app.game_logic import GameManager, TicTacToeGame


# Configure logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'tictactoe_{datetime.now().strftime("%Y%m%d")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize game manager
game_manager = GameManager()


@app.route('/game', methods=['POST'])
def create_game():
    """Create a new game"""
    try:
        game = game_manager.create_game()
        logger.info(f"Created new game: {game.game_id}")
        
        response = {
            'game_id': game.game_id,
            'board': game.board,
            'status': game.status,
            'message': 'Game created successfully. You are X, server is O. Make your move!'
        }
        return jsonify(response), 201
        
    except Exception as e:
        logger.error(f"Error creating game: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/games', methods=['GET'])
def get_all_games():
    """Get all games in chronological order"""
    try:
        games = game_manager.get_all_games()
        logger.info(f"Retrieved {len(games)} games")
        
        games_summary = []
        for game in games:
            games_summary.append({
                'game_id': game.game_id,
                'status': game.status,
                'winner': game.winner,
                'board': game.board,
                'created_at': game.created_at.isoformat() + 'Z'
            })
            
        return jsonify({'games': games_summary}), 200
        
    except Exception as e:
        logger.error(f"Error retrieving games: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/game/<game_id>/move', methods=['POST'])
def make_move(game_id):
    """Player makes a move"""
    try:
        # Get game
        game = game_manager.get_game(game_id)
        if not game:
            logger.warning(f"Game not found: {game_id}")
            return jsonify({'error': 'Game not found'}), 404
            
        # Check if game is already finished
        if game.status != 'in_progress':
            logger.info(f"Attempted move on finished game: {game_id}")
            return jsonify({
                'error': 'Game is already finished',
                'game_id': game.game_id,
                'board': game.board,
                'status': game.status,
                'winner': game.winner,
                'message': f'Game is {game.status}'
            }), 400
            
        # Parse request
        data = request.get_json()
        if not data or 'row' not in data or 'col' not in data:
            logger.warning(f"Invalid move request for game {game_id}: missing row or col")
            return jsonify({'error': 'Invalid request', 'details': 'row and col are required'}), 400
            
        row = data['row']
        col = data['col']
        
        # Validate input
        if not isinstance(row, int) or not isinstance(col, int):
            return jsonify({'error': 'Invalid request', 'details': 'row and col must be integers'}), 400
            
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return jsonify({'error': 'Invalid move', 'details': 'row and col must be between 0 and 2'}), 400
            
        # Make player move
        if not game.make_move(row, col, TicTacToeGame.PLAYER):
            logger.warning(f"Invalid move for game {game_id}: ({row}, {col})")
            return jsonify({'error': 'Invalid move', 'details': 'Position is already occupied or invalid'}), 400
            
        logger.info(f"Player move in game {game_id}: ({row}, {col})")
        
        # Check if player won
        game.update_status()
        if game.status != 'in_progress':
            logger.info(f"Game {game_id} finished after player move: {game.status}")
            return jsonify({
                'game_id': game.game_id,
                'board': game.board,
                'status': game.status,
                'winner': game.winner,
                'message': f'Game over! Result: {game.status}'
            }), 200
            
        # Server makes move
        server_move = game.make_random_move()
        if server_move:
            logger.info(f"Server move in game {game_id}: {server_move}")
        
        # Check game status after server move
        game.update_status()
        
        message = 'Your turn!' if game.status == 'in_progress' else f'Game over! Result: {game.status}'
        logger.info(f"Game {game_id} status after server move: {game.status}")
        
        return jsonify({
            'game_id': game.game_id,
            'board': game.board,
            'status': game.status,
            'winner': game.winner,
            'message': message
        }), 200
        
    except Exception as e:
        logger.error(f"Error making move in game {game_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/game/<game_id>/moves', methods=['GET'])
def get_game_moves(game_id):
    """Get all moves for a game"""
    try:
        game = game_manager.get_game(game_id)
        if not game:
            logger.warning(f"Game not found: {game_id}")
            return jsonify({'error': 'Game not found'}), 404
            
        moves = game.get_moves()
        logger.info(f"Retrieved {len(moves)} moves for game {game_id}")
        
        return jsonify({
            'game_id': game_id,
            'moves': moves
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving moves for game {game_id}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


def run_server(host='0.0.0.0', port=5000, debug=False):
    """Run the Flask server"""
    logger.info(f"Starting Tic-Tac-Toe server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)

