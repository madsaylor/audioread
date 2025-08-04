# AudioRead

A text-to-speech application with synchronized word highlighting that converts text to natural-sounding speech using ElevenLabs API and provides real-time visual feedback during audio playback.

## Features

- **Text-to-Speech**: Generate natural-sounding audio using ElevenLabs multilingual TTS
- **Word Synchronization**: Real-time word highlighting synchronized with audio playback
- **Interactive Playback**: Audio controls with word-level timing information
- **Modern UI**: Clean, responsive interface built with Vue 3 and Bootstrap

## Technology Stack

- **Frontend**: Vue 3 (Composition API), Vite, Bootstrap 5, Howler.js
- **Backend**: Flask, ElevenLabs API
- **Reverse Proxy**: Caddy web server for SSL termination and routing
- **Deployment**: Docker Compose

## Quick Start

### Using Docker (Recommended)

```bash
docker compose up
```

This will start all services with Caddy reverse proxy on http://localhost:8088.

### Manual Setup

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```
The Flask server will run on port 5000 (accessible through Caddy proxy).

#### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
The Vue application will run on http://localhost:5173 (accessible through Caddy proxy).

## Usage

1. Enter text in the input field
2. Click "Generate Speech" to create audio with ElevenLabs TTS
3. Play the audio and watch words highlight in real-time
4. Use playback controls to navigate through the audio

## Configuration

The ElevenLabs API key is currently hardcoded in `backend/app.py`. For production use, move this to environment variables.

## API Endpoints

- `POST /tts` - Generate text-to-speech audio with word timing
- `GET /audio/<path>` - Serve generated audio files

## Development

### Start Development Environment
```bash
docker compose up
```
This starts all services with:
- Application: http://localhost:8088 (Caddy reverse proxy)
- Frontend: Direct access via volume mount with hot reload
- Backend: Direct access via volume mount with hot reload

### Development Commands
```bash
# Start services in detached mode
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild containers (after dependency changes)
docker compose up --build

# Access container shell for debugging
docker compose exec frontend sh
docker compose exec backend bash
docker compose exec caddy sh
```

### Development Notes
- Both frontend and backend have volume mounts for hot reloading
- Frontend uses Vite dev server with HMR
- Backend Flask app auto-reloads on file changes
- Audio files are stored in `backend/audio/` directory