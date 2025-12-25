# Tic-Tac-Toe Deployment Guide

This guide provides detailed instructions for setting up and deploying the Tic-Tac-Toe web service.

## Table of Contents

- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Using the CLI Client](#using-the-cli-client)
- [Monitoring and Logs](#monitoring-and-logs)
- [API Testing](#api-testing)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **RAM**: 512 MB minimum
- **Disk Space**: 50 MB minimum
- **Network**: Port 5000 available (or any other port of your choice)

### Recommended

- **Python**: 3.10 or higher
- **RAM**: 1 GB or more
- **Virtual Environment**: For dependency isolation

## Installation

### Step 1: Clone or Download the Project

If you have the project in a repository:
```bash
git clone <repository-url>
cd ethtca-tic-tac-toe
```

Or if you have the project as a directory, navigate to it:
```bash
cd ethtca-tic-tac-toe
```

### Step 2: Create a Virtual Environment (Recommended)

#### On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Verify installation:
```bash
pip list
```

You should see Flask, pytest, requests, and flask-cors in the list.

## Running the Server

### Development Mode

Start the server in development mode (with auto-reload):

```bash
python -m app.server
```

Or:

```bash
python app/server.py
```

The server will start on `http://0.0.0.0:5000` by default.

**Output:**
```
INFO - Starting Tic-Tac-Toe server on 0.0.0.0:5000
 * Serving Flask app 'server'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### Production Mode

For production, use a WSGI server like Gunicorn:

#### Install Gunicorn:
```bash
pip install gunicorn
```

#### Run with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app.server:app
```

Parameters:
- `-w 4`: Use 4 worker processes
- `-b 0.0.0.0:5000`: Bind to all interfaces on port 5000

### Custom Port

To run on a different port, modify the server startup:

```python
# In app/server.py, change the last line to:
if __name__ == '__main__':
    run_server(host='0.0.0.0', port=8080, debug=True)
```

Or with Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8080 app.server:app
```

### Running in Background

#### On Linux/macOS:
```bash
nohup python -m app.server > server.log 2>&1 &
```

To stop:
```bash
pkill -f "python -m app.server"
```

#### Using systemd (Linux):

Create `/etc/systemd/system/tictactoe.service`:

```ini
[Unit]
Description=Tic-Tac-Toe Game Server
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/ethtca-tic-tac-toe
ExecStart=/path/to/venv/bin/python -m app.server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start tictactoe
sudo systemctl enable tictactoe
sudo systemctl status tictactoe
```

## Configuration

### Logging Configuration

Logs are automatically created in the `logs/` directory. The log file naming convention is:
```
logs/tictactoe_YYYYMMDD.log
```

To change log configuration, edit `app/server.py`:

```python
# Change log level
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG, INFO, WARNING, ERROR
    ...
)

# Change log file location
log_dir = '/var/log/tictactoe'  # Custom path
```

### CORS Configuration

CORS is enabled by default for all origins. To restrict origins, modify `app/server.py`:

```python
# Restrict to specific origins
CORS(app, origins=["http://localhost:3000", "http://example.com"])
```

## Running Tests

### Run All Tests

```bash
pytest tests/
```

### Run with Verbose Output

```bash
pytest tests/ -v
```

### Run with Coverage Report

```bash
pip install pytest-cov
pytest tests/ --cov=app --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # On macOS
xdg-open htmlcov/index.html  # On Linux
```

### Run Specific Test File

```bash
pytest tests/test_game_logic.py
```

### Run Specific Test Function

```bash
pytest tests/test_game_logic.py::TestTicTacToeGame::test_check_winner_row
```

### Expected Output

```
======================== test session starts ========================
collected 25 items

tests/test_game_logic.py::TestTicTacToeGame::test_game_initialization PASSED
tests/test_game_logic.py::TestTicTacToeGame::test_make_valid_move PASSED
...
======================== 25 passed in 0.15s ========================
```

## Using the CLI Client

### Basic Usage

```bash
python client.py
```

### Custom Server URL

```bash
python client.py http://192.168.1.100:5000
```

### Make Client Executable (Linux/macOS)

```bash
chmod +x client.py
./client.py
```

## Monitoring and Logs

### Log Files

Logs are stored in `logs/tictactoe_YYYYMMDD.log`. Each day creates a new log file.

### View Real-time Logs

```bash
tail -f logs/tictactoe_$(date +%Y%m%d).log
```

### Log Rotation

For production, consider using logrotate (Linux) or a similar tool.

Create `/etc/logrotate.d/tictactoe`:

```
/path/to/ethtca-tic-tac-toe/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 youruser yourgroup
}
```

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy"}
```

## API Testing

### Using curl

#### Create a game:
```bash
curl -X POST http://localhost:5000/game
```

#### Make a move:
```bash
curl -X POST http://localhost:5000/game/game_1/move \
  -H "Content-Type: application/json" \
  -d '{"row": 1, "col": 1}'
```

#### Get moves:
```bash
curl http://localhost:5000/game/game_1/moves
```

#### List all games:
```bash
curl http://localhost:5000/games
```

### Using Postman

1. Import the OpenAPI specification (`openapi.yaml`)
2. Postman will automatically create a collection with all endpoints
3. Set the base URL to `http://localhost:5000`
4. Test each endpoint

### Using Swagger UI

You can use Swagger UI to test the API:

```bash
# Install swagger-ui-bundle
pip install flask-swagger-ui
```

Add to `app/server.py`:

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Tic-Tac-Toe API"}
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
```

Then visit `http://localhost:5000/api/docs`

## Troubleshooting

### Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use a different port
python -m app.server --port 5001
```

### Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission Denied for Logs

**Error:**
```
PermissionError: [Errno 13] Permission denied: 'logs/tictactoe_20241225.log'
```

**Solution:**
```bash
# Create logs directory with proper permissions
mkdir -p logs
chmod 755 logs

# Or run with sudo (not recommended)
sudo python -m app.server
```

### Connection Refused (Client)

**Error:**
```
Connection error: Connection refused
```

**Solution:**
1. Make sure the server is running
2. Check the server URL and port
3. Verify firewall settings
4. Check server logs for errors

### Import Errors

**Error:**
```
ImportError: attempted relative import with no known parent package
```

**Solution:**
Run the server as a module:
```bash
python -m app.server
# NOT: python app/server.py
```

## Performance Tuning

### For High Load

Use multiple Gunicorn workers:
```bash
gunicorn -w 8 -b 0.0.0.0:5000 --timeout 120 app.server:app
```

### Memory Usage

Monitor memory:
```bash
# On Linux
ps aux | grep python

# On macOS
ps aux | grep python
```

## Security Considerations

1. **Change Default Port**: Don't use port 5000 in production
2. **Restrict CORS**: Don't allow all origins in production
3. **Use HTTPS**: In production, use a reverse proxy (nginx) with SSL
4. **Rate Limiting**: Consider adding rate limiting for production
5. **Input Validation**: Already implemented in the code

## Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.server:app"]
```

Build and run:
```bash
docker build -t tictactoe .
docker run -p 5000:5000 tictactoe
```

## Summary

You should now have:
- ✅ Server running on port 5000
- ✅ CLI client working
- ✅ Tests passing
- ✅ Logs being generated
- ✅ API endpoints accessible

For any issues, check the logs first and refer to the troubleshooting section.

Happy gaming!

