# Tic-Tac-Toe User Manual

Welcome to the Tic-Tac-Toe game! This guide will help you play the game using the CLI client.

## Getting Started

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

## How to Play

### Game Basics

- You play as **'X'** (the player)
- The server plays as **'O'**
- You always make the first move
- The board is 3x3 with positions numbered 0-2 for both rows and columns

### Board Layout

```
     0   1   2
   +---+---+---+
 0 |   |   |   |
   +---+---+---+
 1 |   |   |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+
```

### Position Reference

| Position | Row | Col |
|----------|-----|-----|
| Top-Left | 0 | 0 |
| Top-Center | 0 | 1 |
| Top-Right | 0 | 2 |
| Middle-Left | 1 | 0 |
| Center | 1 | 1 |
| Middle-Right | 1 | 2 |
| Bottom-Left | 2 | 0 |
| Bottom-Center | 2 | 1 |
| Bottom-Right | 2 | 2 |

## CLI Commands

### Creating a New Game

```
> new
```

This creates a new game and displays an empty board. You'll receive a game ID.

**Example:**
```
> new

✓ New game created: game_1
Game created successfully. You are X, server is O. Make your move!
     0   1   2
   +---+---+---+
 0 |   |   |   |
   +---+---+---+
 1 |   |   |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+
```

### Making a Move

```
> move <row> <col>
```

Place your mark at the specified position. The server will automatically respond with its move.

**Example:**
```
> move 1 1

✓ Move made at (1, 1)
     0   1   2
   +---+---+---+
 0 |   | O |   |
   +---+---+---+
 1 |   | X |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+
Status: in_progress
Your turn!
```

### Viewing Move History

View all moves for the current game:
```
> moves
```

View moves for a specific game:
```
> moves game_1
```

**Example:**
```
> moves

=== Moves for game game_1 ===
1. PLAYER -> (1, 1) at 2024-12-25T10:30:00.123Z
2. SERVER -> (0, 1) at 2024-12-25T10:30:00.456Z
```

### Listing All Games

```
> list
```

This shows all games you've played, including their final states.

**Example:**
```
> list

=== All Games (2 total) ===

Game ID: game_1
  Status: player_wins
  Winner: player
  Created: 2024-12-25T10:25:00.000Z
  Final board:
       0   1   2
     +---+---+---+
   0 | X | O |   |
     +---+---+---+
   1 | X | O |   |
     +---+---+---+
   2 | X |   |   |
     +---+---+---+

Game ID: game_2
  Status: in_progress
  Winner: N/A
  Created: 2024-12-25T10:30:00.000Z
  Final board:
       0   1   2
     +---+---+---+
   0 |   | O |   |
     +---+---+---+
   1 |   | X |   |
     +---+---+---+
   2 |   |   |   |
     +---+---+---+
```

### Getting Help

```
> help
```

Displays all available commands and examples.

### Exiting the Client

```
> quit
```

or

```
> exit
```

You can also press `Ctrl+C` to exit.

## Game Flow Example

Here's a complete game example:

```
> new
✓ New game created: game_1
Game created successfully. You are X, server is O. Make your move!
     0   1   2
   +---+---+---+
 0 |   |   |   |
   +---+---+---+
 1 |   |   |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+

> move 1 1
✓ Move made at (1, 1)
     0   1   2
   +---+---+---+
 0 | O |   |   |
   +---+---+---+
 1 |   | X |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+
Status: in_progress
Your turn!

> move 0 1
✓ Move made at (0, 1)
     0   1   2
   +---+---+---+
 0 | O | X |   |
   +---+---+---+
 1 | O | X |   |
   +---+---+---+
 2 |   |   |   |
   +---+---+---+
Status: in_progress
Your turn!

> move 2 1
✓ Move made at (2, 1)
     0   1   2
   +---+---+---+
 0 | O | X |   |
   +---+---+---+
 1 | O | X |   |
   +---+---+---+
 2 |   | X |   |
   +---+---+---+
Status: player_wins
Winner: player
Game over! Result: player_wins

Game game_1 has ended.
```

## Winning the Game

You win by getting three of your marks (X) in a row:

- **Horizontally**: Any row with three X's
- **Vertically**: Any column with three X's
- **Diagonally**: Either diagonal with three X's

The server (O) wins the same way. If all positions are filled with no winner, the game is a draw.

## Tips

1. **Center Control**: The center position (1, 1) is often strategic
2. **Block the Server**: Watch for the server's potential winning moves
3. **Think Ahead**: Plan your moves to create multiple winning opportunities
4. **Review Games**: Use the `list` command to review past games and learn

## Common Errors

### "No active game"
You need to create a game first with the `new` command.

### "Invalid move"
The position is already occupied or out of bounds (0-2 range).

### "Game is already finished"
You're trying to move in a completed game. Create a new game with `new`.

### "Connection error"
The server is not running or not accessible. Make sure the server is started.

## Using the REST API Directly

If you prefer to use the API directly (e.g., with curl or Postman), refer to the `openapi.yaml` specification file for complete API documentation.

### Example with curl

Create a game:
```bash
curl -X POST http://localhost:5000/game
```

Make a move:
```bash
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 1, "col": 1}'
```

Get all moves:
```bash
curl http://localhost:5000/game/game_1/moves
```

List all games:
```bash
curl http://localhost:5000/games
```

## Troubleshooting

If you encounter issues:

1. Check that the server is running
2. Verify you're using the correct server URL
3. Check the server logs in the `logs/` directory
4. Make sure your moves are valid (row and col between 0-2)
5. Ensure the game is still in progress before making moves

## Support

For technical issues, check:
- Server logs in `logs/tictactoe_YYYYMMDD.log`
- API specification in `openapi.yaml`
- Server implementation in `app/server.py`

Enjoy playing Tic-Tac-Toe!

