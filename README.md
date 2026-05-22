# Real-Time Multilingual Voice AI Agent

## Features
- Real-time voice interaction
- English/Hindi/Tamil support
- Appointment booking
- Rescheduling & cancellation
- PostgreSQL memory storage
- Context-aware conversations
- Conflict resolution
- Low latency pipeline

## Tech Stack
Frontend:
- React + TypeScript

Backend:
- FastAPI
- Python

Database:
- PostgreSQL

Voice:
- Whisper STT
- TTS
- OpenAI/Groq LLM

## Architecture
(Add architecture image here)

## Setup Instructions
Frontend setup
Backend setup
Database setup

## Memory Design
- Session memory
- Persistent patient history
- Language preference retention

## Latency Breakdown
Example:
- STT: 120ms
- LLM: 180ms
- TTS: 100ms
- Total: ~400ms

## Conflict Handling
- Prevent double booking
- Validate future dates
- Suggest alternate slots

## Known Limitations
- No Redis TTL
- Whisper may delay on low CPU
- Limited outbound automation

## Future Improvements
- Redis caching
- SIP calling
- Better Tamil STT
- Kubernetes deployment