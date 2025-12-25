# API Examples

This document provides practical examples of using the Tic-Tac-Toe REST API.

## Prerequisites

Make sure the server is running:
```bash
python -m app.server
```

## Using curl

### 1. Create a New Game

**Request:**
```bash
curl -X POST http://localhost:5000/game \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "game_id": "game_1",
  "board": [[null, null, null], [null, null, null], [null, null, null]],
  "status": "in_progress",
  "message": "Game created successfully. You are X, server is O. Make your move!"
}
```

### 2. Make a Move

**Request:**
```bash
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 1, "col": 1}'
```

**Response:**
```json
{
  "game_id": "game_1",
  "board": [["O", null, null], [null, "X", null], [null, null, null]],
  "status": "in_progress",
  "winner": null,
  "message": "Your turn!"
}
```

### 3. Get Game Moves

**Request:**
```bash
curl http://localhost:5000/game/game_1/moves
```

**Response:**
```json
{
  "game_id": "game_1",
  "moves": [
    {
      "player": "player",
      "position": {"row": 1, "col": 1},
      "timestamp": "2024-12-25T10:30:00.123Z"
    },
    {
      "player": "server",
      "position": {"row": 0, "col": 0},
      "timestamp": "2024-12-25T10:30:00.456Z"
    }
  ]
}
```

### 4. List All Games

**Request:**
```bash
curl http://localhost:5000/games
```

**Response:**
```json
{
  "games": [
    {
      "game_id": "game_1",
      "status": "in_progress",
      "winner": null,
      "board": [["O", null, null], [null, "X", null], [null, null, null]],
      "created_at": "2024-12-25T10:25:00.000Z"
    }
  ]
}
```

### 5. Health Check

**Request:**
```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Complete Game Example

Here's a complete game from start to finish:

```bash
# Create a game
GAME_RESPONSE=$(curl -s -X POST http://localhost:5000/game)
GAME_ID=$(echo $GAME_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['game_id'])")
echo "Created game: $GAME_ID"

# Move 1: Player at center (1,1)
echo "\nMove 1: Player at (1,1)"
curl -s -X POST http://localhost:5000/game/$GAME_ID/move \
  -H "Content-Type: application/json" \
  -d '{"row": 1, "col": 1}' | python3 -m json.tool

# Move 2: Player at top-left (0,0)
echo "\nMove 2: Player at (0,0)"
curl -s -X POST http://localhost:5000/game/$GAME_ID/move \
  -H "Content-Type: application/json" \
  -d '{"row": 0, "col": 0}' | python3 -m json.tool

# Move 3: Player at bottom-right (2,2)
echo "\nMove 3: Player at (2,2)"
curl -s -X POST http://localhost:5000/game/$GAME_ID/move \
  -H "Content-Type: application/json" \
  -d '{"row": 2, "col": 2}' | python3 -m json.tool

# Get all moves
echo "\nAll moves:"
curl -s http://localhost:5000/game/$GAME_ID/moves | python3 -m json.tool

# List all games
echo "\nAll games:"
curl -s http://localhost:5000/games | python3 -m json.tool
```

## Using Python requests

```python
import requests
import json

base_url = "http://localhost:5000"

# Create a game
response = requests.post(f"{base_url}/game")
game_data = response.json()
game_id = game_data['game_id']
print(f"Created game: {game_id}")

# Make a move
move_data = {"row": 1, "col": 1}
response = requests.post(
    f"{base_url}/game/{game_id}/move",
    json=move_data
)
print(f"Move response: {json.dumps(response.json(), indent=2)}")

# Get moves
response = requests.get(f"{base_url}/game/{game_id}/moves")
print(f"Moves: {json.dumps(response.json(), indent=2)}")

# List all games
response = requests.get(f"{base_url}/games")
print(f"All games: {json.dumps(response.json(), indent=2)}")
```

## Using JavaScript (fetch)

```javascript
const baseUrl = 'http://localhost:5000';

// Create a game
fetch(`${baseUrl}/game`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => {
    console.log('Created game:', data.game_id);
    return data.game_id;
  })
  .then(gameId => {
    // Make a move
    return fetch(`${baseUrl}/game/${gameId}/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ row: 1, col: 1 })
    });
  })
  .then(response => response.json())
  .then(data => console.log('Move response:', data));
```

## Error Responses

### Invalid Move (Position Occupied)

**Request:**
```bash
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 1, "col": 1}'
```

**Response (400):**
```json
{
  "error": "Invalid move",
  "details": "Position is already occupied or invalid"
}
```

### Game Not Found

**Request:**
```bash
curl http://localhost:5000/game/nonexistent/moves
```

**Response (404):**
```json
{
  "error": "Game not found"
}
```

### Invalid Input

**Request:**
```bash
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 5, "col": 1}'
```

**Response (400):**
```json
{
  "error": "Invalid move",
  "details": "row and col must be between 0 and 2"
}
```

### Game Already Finished

**Request:**
```bash
# Trying to move in a finished game
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 2, "col": 2}'
```

**Response (400):**
```json
{
  "error": "Game is already finished",
  "game_id": "game_1",
  "board": [["X", "O", null], ["X", "O", null], ["X", null, null]],
  "status": "player_wins",
  "winner": "player",
  "message": "Game is player_wins"
}
```

## Testing with Postman

1. Import the OpenAPI specification (`openapi.yaml`) into Postman
2. Postman will create a collection with all endpoints
3. Set environment variable: `base_url = http://localhost:5000`
4. Run requests in order:
   - Create Game
   - Make Move (repeat as needed)
   - Get Moves
   - List Games

## Testing with HTTPie

If you have HTTPie installed:

```bash
# Create game
http POST localhost:5000/game

# Make move
http POST localhost:5000/game/game_1/move row:=1 col:=1

# Get moves
http GET localhost:5000/game/game_1/moves

# List games
http GET localhost:5000/games
```

## Response Status Codes

| Status Code | Meaning | When |
|-------------|---------|------|
| 200 | OK | Successful GET or move |
| 201 | Created | Game created |
| 400 | Bad Request | Invalid move or input |
| 404 | Not Found | Game doesn't exist |
| 500 | Server Error | Internal error |

## Tips

1. **Save game_id**: After creating a game, save the `game_id` for subsequent requests
2. **Check status**: Always check the `status` field to see if game is finished
3. **Board format**: Board is 3x3 array, null = empty, "X" = player, "O" = server
4. **Move format**: Positions are 0-indexed (0, 1, 2 for both row and col)
5. **Server moves automatically**: After your move, check the board for server's move

## Automation Script

Save this as `play_game.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:5000"

# Create game
echo "Creating game..."
RESPONSE=$(curl -s -X POST $BASE_URL/game)
GAME_ID=$(echo $RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['game_id'])")
echo "Game ID: $GAME_ID"

# Function to make a move
make_move() {
  ROW=$1
  COL=$2
  echo "\nMaking move at ($ROW, $COL)..."
  curl -s -X POST $BASE_URL/game/$GAME_ID/move \
    -H "Content-Type: application/json" \
    -d "{\"row\": $ROW, \"col\": $COL}" | python3 -m json.tool
}

# Play the game
make_move 1 1
make_move 0 0
make_move 2 2

# Show all moves
echo "\nAll moves:"
curl -s $BASE_URL/game/$GAME_ID/moves | python3 -m json.tool
```

Make it executable and run:
```bash
chmod +x play_game.sh
./play_game.sh
```

## Summary

The API is simple and intuitive:
- Create game → Get game_id
- Make moves → Server responds automatically
- Query moves/games → Get history

For interactive play, use the CLI client (`python client.py`).
For automation or integration, use the REST API directly.

Enjoy playing!

