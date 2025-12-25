# Tic-Tac-Toe Web Service

A RESTful web service for playing tic-tac-toe against a server, implemented with Flask and Python.
It is developed with Cursor in one hour. This document first introduces the assumptions used
in this implementation, the prompt that is used to generate these artifacts, and the quick guide for
starting the server and play the game in CLI. The details of this service (features, project structure,
APIs, etc.) are then followed.

## Assumptions

- To control the scope of this challenge, this web service will support only a single player that play games sequentially in CLI. Hence, it doesn’t have any feature related with authentication, authorization, score ranking, user management, etc. It is also out of the scope to support player vs. player game.
- When server acts as the opponent, it is a dummy one and makes move by randomly choosing among available positions.
- Its implementation also doesn’t consider the scalability and persistence. All game states could be stored in the memory.

In general, the output of Cursor is quite good and enable one user to play Tic-Tac-Toe
through CLI. The API can be extended easily to support multiple users. Of course, we
need carry out user management and handle authentication + authorization (through
SSO, maybe). Player vs. Player mode will be more complex and we need decide the
players associated with a game and figure out how to let players get the latest game
status. We can let client pull game state periodically and display to players once the
opponent has moved. However, frequent pulling will waste some resources. We can
also let server push to another player when one player has moved. Note that it will
become necessary to maintain connections with players.

However, player connection management will also become necessary if we need scale
the service to support a large number players. We need deploy multiple servers behind load
balancer or API Gateway. Hence, different players may connect to different servers, and we need
route game state updates to corresponding players. Furthermore, game states should also be moved
from server memory to some distributed cache solution (e.g., Redis). At this stage,
a full-fledged observability solution (e.g., Prometheus + Grafana) will become worthwhile.

## Prompt
```
We need develop a tic-tac-toe web service with Python. The first step is to define its
Rest API using swagger that provides the following interfaces / functions.
- user can generate a new game and return the game id.
- user can make next move by specify the position. The server will act as another player
to make a move and return the new game state so that the user can continue to play.
The server will also complete the game when the result is determined.
- user can query all moves of one specific game, and the server should return these
moves in chronological order.
- user can query all games that had been played, and the server should return these
games (including game id, the result, and the final state) in chronological order.

The second step is to generate the server stub with swagger codegen. Please also
implement this web service with Flask framework. Below are several requirements on
this implementation as a standalone server.
- The server supports only a single player. Hence, please don't bother with user
management.
- We need not store the history of games permanently. Hence, all states can be stored in
memory and persistence layer is unnecessary.
- We need not provide a full-fledged observability solution. However, proper log should
be generated and stored in local storage for diagnosis purpose.
- Unit tests should be written to validate critical business logic.
- When server acts as another player, it can choose among available positions
randomly.

The third step is to generate one client so that player can play the game with CLI.

Finally, please generate corresponding documents, such as the manual for the player
and the steps for launching the service.
```

## Quick Start

### 1. Start the Server

```bash
./run_server.sh
```

The server will start on `http://localhost:5000`

### 2. Play with CLI Client

In a new terminal:

```bash
./run_client.sh
```

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

