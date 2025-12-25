# Tic-Tac-Toe Web Service

A RESTful web service for playing tic-tac-toe against a server, implemented with Flask and Python.

## Features

- **REST API**: Well-defined REST API following OpenAPI 3.0 specification
- **Single Player Mode**: Play against the server (server makes random moves)
- **In-Memory Storage**: All game states stored in memory (no database required)
- **Comprehensive Logging**: All operations logged to local storage for diagnosis
- **CLI Client**: Interactive command-line interface for playing games
- **Unit Tests**: Comprehensive test coverage for critical business logic

## Project Structure

```
ethtca-tic-tac-toe/
├── openapi.yaml           # OpenAPI/Swagger specification
├── requirements.txt       # Python dependencies
├── app/
│   ├── __init__.py
│   ├── server.py         # Flask server implementation
│   └── game_logic.py     # Tic-tac-toe game logic
├── tests/
│   ├── __init__.py
│   └── test_game_logic.py  # Unit tests
├── client.py             # CLI client
├── logs/                 # Log files (created at runtime)
├── README.md            # This file
├── USER_MANUAL.md       # User manual for playing
└── DEPLOYMENT.md        # Deployment and setup guide
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python -m app.server
```

The server will start on `http://localhost:5000`

### 3. Play with CLI Client

In a new terminal:

```bash
python client.py
```

### 4. Run Tests

```bash
pytest tests/
```

## API Endpoints

- `POST /game` - Create a new game
- `POST /game/{game_id}/move` - Make a move
- `GET /game/{game_id}/moves` - Get all moves for a game
- `GET /games` - Get all games
- `GET /health` - Health check

## Documentation

- **[User Manual](USER_MANUAL.md)** - How to play the game
- **[Deployment Guide](DEPLOYMENT.md)** - Server setup and configuration
- **[API Specification](openapi.yaml)** - Complete OpenAPI specification

## Technology Stack

- **Python 3.8+**
- **Flask** - Web framework
- **Pytest** - Testing framework
- **Requests** - HTTP client for CLI

## Game Rules

- Player is 'X', Server is 'O'
- Player always moves first
- Server automatically responds after player's move
- Game ends when:
  - A player gets three in a row (horizontally, vertically, or diagonally)
  - All positions are filled (draw)

## Logging

Logs are stored in the `logs/` directory with the format:
- Filename: `tictactoe_YYYYMMDD.log`
- Contains all API requests, game operations, and errors

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions, please check the logs in the `logs/` directory for diagnostic information.

