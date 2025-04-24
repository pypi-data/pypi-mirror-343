# Sonos to Last.fm Scrobbler

![sonos lastfm](https://github.com/user-attachments/assets/6c84174d-a927-4801-8800-e2343d1646d7)

This script automatically scrobbles music playing on your Sonos speakers to Last.fm.

## Features

- Automatic Sonos speaker discovery on your network
- Real-time track monitoring and scrobbling
- Smart duplicate scrobble prevention
- Multi-speaker support
- Local data persistence for tracking scrobble history
- Secure credential storage using system keyring
- Modern CLI interface with interactive setup

## Detailed Features

### Scrobbling Logic

The script follows configurable scrobbling rules:
- A track is scrobbled when either:
  - Configured percentage of the track has been played (default: 25%, range: 0-100), OR
  - 4 minutes (240 seconds) of the track have been played
- For repeated plays of the same track:
  - Enforces a 30-minute minimum interval between scrobbles of the same track
  - Prevents duplicate scrobbles during continuous play

### Track Monitoring

- Continuously monitors all Sonos speakers on the network
- Tracks playback position and duration for each speaker
- Only scrobbles tracks that are actually playing (ignores paused/stopped states)
- Requires both artist and title information to be present for scrobbling

### Data Storage

- Maintains persistent storage in the `./data` directory:
  - `last_scrobbled.json`: Records of recently scrobbled tracks
  - `currently_playing.json`: Current playback state for each speaker
- Prevents data loss across script restarts

## Setup

### Option 1: Install from PyPI (Recommended)

```bash
pip install sonos-lastfm
```

### Option 2: Local Development Setup

1. Install `uv` (Python package installer):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Setup and run using Make commands:
   ```bash
   # Setup Python environment with uv
   make setup

   # Install dependencies
   make install

   # For development, install additional tools (optional)
   make install-dev
   ```

   Run `make help` to see all available commands.

### Option 3: Docker Setup (Recommended for Linux)

> Note: Docker setup is not recommended on macOS due to network mode limitations affecting Sonos discovery.

1. Create a `.env` file with your Last.fm credentials:
   ```bash
   LASTFM_USERNAME=your_username
   LASTFM_PASSWORD=your_password
   LASTFM_API_KEY=your_api_key
   LASTFM_API_SECRET=your_api_secret
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

   This will:
   - Build the container with all dependencies
   - Run in network host mode for Sonos discovery
   - Persist data across container restarts
   - Automatically restart on failure

### Manual Setup (Alternative)

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get your Last.fm API credentials:
   - Go to https://www.last.fm/api/account/create
   - Create a new API account
   - Note down your API key and API secret

3. Configure the script:
   - Open `config.py`
   - Fill in your Last.fm credentials:
     - `LASTFM_USERNAME`: Your Last.fm username
     - `LASTFM_PASSWORD`: Your Last.fm password
     - `LASTFM_API_KEY`: Your Last.fm API key
     - `LASTFM_API_SECRET`: Your Last.fm API secret
   - Optionally adjust:
     - `SCROBBLE_INTERVAL` (default: 30 seconds)
     - `SCROBBLE_THRESHOLD_PERCENT` (default: 25%, must be between 0 and 100)

## Usage

### Interactive Setup (Recommended)

Run the interactive setup to securely store your Last.fm credentials:

```bash
sonos-lastfm --setup
```

This will:
1. Prompt for your Last.fm credentials
2. Store them securely in your system keyring
3. Create necessary configuration directories

### Command Line Options

```bash
sonos-lastfm [OPTIONS]

Options:
  -u, --username TEXT            Last.fm username
  -p, --password TEXT           Last.fm password
  -k, --api-key TEXT           Last.fm API key
  -s, --api-secret TEXT        Last.fm API secret
  -i, --interval INTEGER       Scrobbling check interval in seconds [default: 1]
  -r, --rediscovery INTEGER    Speaker rediscovery interval in seconds [default: 10]
  -t, --threshold FLOAT        Scrobble threshold percentage [default: 25.0]
  --setup                      Run interactive setup
  --help                       Show this message and exit
```

### Configuration Priority

The scrobbler looks for configuration in the following order:
1. Command line arguments
2. Environment variables
3. Securely stored credentials in system keyring

### Environment Variables

You can also configure the scrobbler using environment variables:

```bash
export LASTFM_USERNAME=your_username
export LASTFM_PASSWORD=your_password
export LASTFM_API_KEY=your_api_key
export LASTFM_API_SECRET=your_api_secret
export SCROBBLE_INTERVAL=1
export SPEAKER_REDISCOVERY_INTERVAL=10
export SCROBBLE_THRESHOLD_PERCENT=25
```

The script will:
1. Create necessary data directories
2. Discover Sonos speakers on your network
3. Monitor currently playing tracks
4. Scrobble new tracks to Last.fm according to the scrobbling rules
5. Log all activities to the console with a nice progress display

## Requirements

- Python 3.11+
- Sonos speakers on your network
- Last.fm account
- Last.fm API credentials

## Troubleshooting

Common issues and solutions:
- No speakers found: Ensure your computer is on the same network as your Sonos system
- Scrobbling not working: Check your Last.fm credentials with `sonos-lastfm --setup`
- Missing scrobbles: Verify that both artist and title information are available for the track
