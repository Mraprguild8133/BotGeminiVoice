# Educational Telegram Voice Assistant Bot

## Overview

This is an educational Telegram bot powered by Google Gemini AI, designed to provide programming education and coding support. The bot supports both voice and text interactions, offering features like code analysis, debugging assistance, educational tutorials, and multi-language programming support. It processes voice messages through speech-to-text conversion and can respond with both text and audio explanations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Core Design Pattern
The application follows a modular architecture with clear separation of concerns:

- **Main Entry Point**: `main.py` serves as the application launcher with environment validation
- **Bot Core**: `TelegramBot` class orchestrates all bot interactions and message routing
- **AI Integration**: `GeminiAssistant` handles educational AI responses with a specialized teaching prompt
- **Specialized Processors**: Dedicated modules for voice processing, code analysis, and educational content

### Communication Flow
1. **Message Reception**: Telegram webhook receives user messages (text/voice)
2. **Processing Pipeline**: Messages are routed to appropriate processors based on type
3. **AI Processing**: Educational queries are sent to Gemini AI with educational context
4. **Response Generation**: Formatted responses are sent back to users via Telegram

### Voice Processing Architecture
- **Speech-to-Text**: Uses `speech_recognition` library for converting voice messages
- **Audio Handling**: PyAudio and ffmpeg for audio format conversion and processing
- **Text-to-Speech**: Pyttsx3 engine for generating audio responses with educational-friendly settings

### Code Analysis System
- **Language Detection**: Pattern-based detection supporting 10+ programming languages
- **Syntax Analysis**: Automated code review with educational feedback
- **Code Formatting**: Pygments-based syntax highlighting for improved readability

### Educational Content Management
- **Structured Tutorials**: Organized programming content by language and difficulty
- **Learning Paths**: Progressive educational material delivery
- **Best Practices**: Industry-standard coding recommendations integrated into responses

## External Dependencies

### AI Services
- **Google Gemini AI**: Primary AI model for educational responses and code assistance
- **Gemini API**: RESTful API integration for natural language processing

### Telegram Integration
- **python-telegram-bot**: Official Python library for Telegram Bot API
- **Telegram Bot API**: Real-time messaging and file handling capabilities

### Voice Processing
- **speech_recognition**: Speech-to-text conversion library
- **pyttsx3**: Cross-platform text-to-speech synthesis
- **PyAudio**: Real-time audio I/O for voice processing
- **ffmpeg**: Audio format conversion and processing

### Code Processing
- **Pygments**: Syntax highlighting and code formatting
- **Regular Expressions**: Pattern matching for language detection and code analysis

### Infrastructure
- **python-dotenv**: Environment variable management for API keys
- **Standard Logging**: Built-in Python logging with custom formatters
- **File System**: Temporary file handling for audio processing