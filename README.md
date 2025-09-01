# Educational Telegram Voice Assistant Bot

An advanced educational Telegram bot powered by Google Gemini AI, designed for programming education and coding support. Created by **Mraprguild**.

## 🎓 Features

### Voice & Text Interaction
- **Voice Message Processing**: Send coding questions via voice messages
- **Speech-to-Text**: Advanced voice recognition for programming queries
- **Text-to-Speech**: Audio explanations for educational content
- **Multi-modal Support**: Both voice and text-based conversations

### AI-Powered Coding Assistance
- **Google Gemini 2.5 Integration**: Latest AI model for accurate responses
- **Code Analysis**: Automatic detection and analysis of code snippets
- **Multi-language Support**: Python, JavaScript, Java, C++, HTML, CSS, and more
- **Educational Focus**: Learning-oriented explanations, not just answers

### Educational Features
- **Step-by-step Explanations**: Complex concepts broken down for learners
- **Code Review**: Comprehensive analysis with improvement suggestions
- **Debug Assistance**: Error detection and resolution guidance
- **Programming Tutorials**: Interactive learning paths for different topics
- **Best Practices**: Industry-standard coding recommendations

### Code Processing
- **Syntax Highlighting**: Beautiful code formatting with language detection
- **Error Detection**: Common mistake identification and fixes
- **Performance Analysis**: Code quality metrics and optimization tips
- **File Upload Support**: Analyze complete code files (.py, .js, .java, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Google Gemini API key
- Audio processing libraries (optional for voice features)

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd telegram-edu-bot
   ```

2. **Install Dependencies**
   ```bash
   pip install python-telegram-bot google-genai speech_recognition pyttsx3 python-dotenv pygments pyaudio pydub
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your tokens and API keys
   ```

4. **Run the Bot**
   ```bash
   python main.py
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following required variables:

```env
# Required
BOT_TOKEN=your_telegram_bot_token_from_botfather
GEMINI_API_KEY=your_gemini_api_key_from_google

# Optional
LOG_LEVEL=INFO
ENABLE_VOICE_RESPONSES=true
AUDIO_QUALITY=high
