# Quick Start Guide

Get up and running with Tic-Tac-Toe in 3 simple steps!

## Option 1: Using Shell Scripts (Linux/macOS)

### Step 1: Make scripts executable
```bash
chmod +x run_server.sh run_client.sh run_tests.sh
```

### Step 2: Start the server
```bash
./run_server.sh
```

### Step 3: In a new terminal, start the client
```bash
./run_client.sh
```

### (Optional) Run tests
```bash
./run_tests.sh
```

## Option 2: Manual Setup

### Step 1: Install dependencies
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Start the server
```bash
python -m app.server
```

### Step 3: In a new terminal, start the client
```bash
# Activate virtual environment first
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run client
python client.py
```

### (Optional) Run tests
```bash
pytest tests/ -v
```

## Playing Your First Game

Once the client starts, try these commands:

```
> new              # Create a new game
> move 1 1         # Place X in the center
> move 0 0         # Place X in top-left
> moves            # See all moves
> list             # List all games
> help             # Show all commands
> quit             # Exit
```

## What's Next?

- Read the [User Manual](USER_MANUAL.md) for detailed playing instructions
- Check the [Deployment Guide](DEPLOYMENT.md) for production setup
- View the [API Specification](openapi.yaml) for API details

## Troubleshooting

**Server won't start?**
- Make sure port 5000 is not already in use
- Check that all dependencies are installed

**Client can't connect?**
- Verify the server is running
- Check the server URL (default: http://localhost:5000)

**Need help?**
- Run `python client.py` and type `help`
- Check logs in `logs/` directory
- Read the full documentation in README.md

Enjoy playing!

