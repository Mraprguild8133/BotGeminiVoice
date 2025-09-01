"""
Main Telegram Bot class handling all bot interactions
"""

import logging
import os
import re
import tempfile
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, 
    CallbackQueryHandler, filters, ContextTypes
)
from telegram.constants import ParseMode

from .voice_processor import VoiceProcessor
from .gemini_assistant import GeminiAssistant
from .code_analyzer import CodeAnalyzer
from .educational_content import EducationalContent
from utils.logger import setup_logger

logger = setup_logger(__name__)

class TelegramBot:
    """Main Telegram Bot class for educational coding assistance"""
    
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.voice_processor = VoiceProcessor()
        self.gemini_assistant = GeminiAssistant()
        self.code_analyzer = CodeAnalyzer()
        self.educational_content = EducationalContent()
        
        # Build the application
        self.app = ApplicationBuilder().token(bot_token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all bot command and message handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("about", self.about_command))
        self.app.add_handler(CommandHandler("languages", self.languages_command))
        self.app.add_handler(CommandHandler("tutorials", self.tutorials_command))
        self.app.add_handler(CommandHandler("debug", self.debug_command))
        self.app.add_handler(CommandHandler("review", self.review_command))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        
        # Callback query handler for inline keyboards
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_text = f"""
🎓 *Welcome to Educational Coding Assistant* 🎓

Hello {user.first_name}! I'm your AI-powered coding tutor created by *Mraprguild*.

🎯 *What I can help you with:*
• 🎤 Voice-based coding questions and explanations
• 💬 Text-based programming discussions
• 🐛 Debug code errors and issues
• 📝 Code review and improvement suggestions
• 📚 Programming tutorials and concept explanations
• 🔍 Multi-language coding support

*🎙️ Try sending me:*
• A voice message with your coding question
• Code snippets for review
• Error messages for debugging
• Programming concepts to explain

*📋 Quick Commands:*
/help - Show all available commands
/languages - See supported programming languages
/tutorials - Browse coding tutorials
/debug - Get help with debugging
/review - Code review assistance
/about - Learn more about this bot

Ready to start learning? Send me your first coding question! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("🎤 Voice Help", callback_data='voice_help')],
            [InlineKeyboardButton("📚 Tutorials", callback_data='tutorials'), 
             InlineKeyboardButton("🔍 Languages", callback_data='languages')],
            [InlineKeyboardButton("🐛 Debug Help", callback_data='debug_help'),
             InlineKeyboardButton("📝 Code Review", callback_data='review_help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 *Educational Coding Assistant Help* 🆘

*🎯 Main Features:*

*🎤 Voice Commands:*
• Send voice messages with coding questions
• Ask for explanations of programming concepts
• Request step-by-step problem solutions
• Get debugging help through voice

*💬 Text Commands:*
• `/start` - Welcome message and quick start
• `/help` - This help message
• `/about` - About this bot and creator
• `/languages` - Supported programming languages
• `/tutorials` - Browse coding tutorials
• `/debug <code>` - Debug code issues
• `/review <code>` - Get code review

*📝 Text Interactions:*
• Send code snippets for analysis
• Ask programming questions
• Request concept explanations
• Share error messages for debugging

*📄 File Support:*
• Send code files (.py, .js, .java, etc.) for review
• Upload error logs for analysis

*🎯 Educational Focus:*
• Step-by-step explanations
• Learning-oriented responses
• Best practices guidance
• Common mistake identification
• Interactive problem solving

*Example Usage:*
1. Send voice: "Explain what recursion is"
2. Text: "How do I fix this Python error?"
3. Upload a .py file for review
4. Use /debug with your buggy code

Created with ❤️ by *Mraprguild*
        """
        
        await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        about_text = """
ℹ️ *About Educational Coding Assistant* ℹ️

*👨‍💻 Creator:* Mraprguild
*🤖 Powered by:* Google Gemini AI
*🎯 Purpose:* Educational programming support and coding assistance

*🌟 Key Features:*
• Advanced AI-powered code analysis
• Voice-to-text coding assistance
• Multi-language programming support
• Educational explanations and tutorials
• Real-time debugging help
• Code review and improvement suggestions

*🎓 Educational Approach:*
• Learn by doing and understanding
• Step-by-step problem breakdown
• Best practices guidance
• Common pitfall identification
• Interactive learning experience

*🔧 Technical Stack:*
• Google Gemini 2.5 Flash/Pro AI
• Advanced speech recognition
• Syntax highlighting and analysis
• Multi-format code processing

*💡 Mission:*
To make programming education accessible, interactive, and effective through AI-powered assistance and voice interaction.

*🤝 Support:*
This bot is designed to supplement your learning journey, not replace formal education. Always practice coding hands-on!

Built with passion for education by *Mraprguild* 🚀
        """
        
        await update.message.reply_text(about_text, parse_mode=ParseMode.MARKDOWN)
    
    async def languages_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /languages command"""
        languages_text = await self.educational_content.get_supported_languages()
        
        keyboard = [
            [InlineKeyboardButton("Python Tutorial", callback_data='tutorial_python')],
            [InlineKeyboardButton("JavaScript Tutorial", callback_data='tutorial_javascript'),
             InlineKeyboardButton("Java Tutorial", callback_data='tutorial_java')],
            [InlineKeyboardButton("C++ Tutorial", callback_data='tutorial_cpp'),
             InlineKeyboardButton("React Tutorial", callback_data='tutorial_react')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            languages_text, 
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def tutorials_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /tutorials command"""
        tutorials_text = await self.educational_content.get_tutorial_menu()
        
        keyboard = [
            [InlineKeyboardButton("Beginner Basics", callback_data='tutorials_beginner')],
            [InlineKeyboardButton("Data Structures", callback_data='tutorials_ds'),
             InlineKeyboardButton("Algorithms", callback_data='tutorials_algo')],
            [InlineKeyboardButton("Web Development", callback_data='tutorials_web'),
             InlineKeyboardButton("Debugging Tips", callback_data='tutorials_debug')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            tutorials_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
    
    async def debug_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /debug command"""
        if context.args:
            code = " ".join(context.args)
            debug_result = await self.code_analyzer.debug_code(code)
            await update.message.reply_text(debug_result, parse_mode=ParseMode.MARKDOWN)
        else:
            debug_help = """
🐛 *Debug Command Help* 🐛

*Usage:* `/debug <your_code_here>`

*Example:*
`/debug print("Hello World")`

*For better debugging:*
• Include complete code snippets
• Mention the programming language
• Describe the expected vs actual behavior
• Share any error messages you're seeing

*Educational support by Mraprguild's AI Assistant* 🔧
            """
            
            await update.message.reply_text(debug_help, parse_mode=ParseMode.MARKDOWN)
    
    async def review_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /review command"""
        if context.args:
            code = " ".join(context.args)
            review_result = await self.code_analyzer.review_code(code)
            await update.message.reply_text(review_result, parse_mode=ParseMode.MARKDOWN)
        else:
            review_help = """
📝 *Code Review Help* 📝

*Usage:* `/review <your_code_here>`

*Example:*
`/review def hello(): print("Hello World")`

*For comprehensive review:*
• Share complete functions or classes
• Mention what the code should accomplish
• Ask specific questions about improvements
• Include the programming language context

*Educational support by Mraprguild's AI Assistant* ⭐
            """
            
            await update.message.reply_text(review_help, parse_mode=ParseMode.MARKDOWN)
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages"""
        try:
            voice = update.message.voice
            if not voice:
                await update.message.reply_text("❌ No voice message found.")
                return
            
            # Send processing message
            processing_msg = await update.message.reply_text("🎤 Processing your voice message...")
            
            # Download voice file
            voice_file = await voice.get_file()
            
            # Process voice to text
            transcribed_text = await self.voice_processor.process_voice_message(voice_file)
            
            if not transcribed_text:
                await processing_msg.edit_text(
                    "❌ **Voice Recognition Failed**\n\n"
                    "I couldn't understand your voice message. Here are some tips:\n\n"
                    "🎤 **Try these improvements:**\n"
                    "• Speak clearly and at a moderate pace\n"
                    "• Record in a quiet environment\n"
                    "• Hold the microphone close to your mouth\n"
                    "• Use simple, clear language\n\n"
                    "📝 **Alternative:** You can also type your programming question!\n\n"
                    "*Educational support by Mraprguild's AI Assistant*",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            
            # Show what was understood
            await processing_msg.edit_text(f"🎯 **I heard:** {transcribed_text}\n\n⏳ Generating educational response...")
            
            # Get AI response
            ai_response = await self.gemini_assistant.get_educational_response(transcribed_text, is_voice=True)
            
            # Send the text response
            await processing_msg.edit_text(ai_response, parse_mode=ParseMode.MARKDOWN)
            
            # Send a follow-up message optimized for voice reading
            try:
                # Create a voice-friendly version of the response
                voice_friendly_text = self.voice_processor._prepare_educational_text(ai_response)
                
                if len(voice_friendly_text) < len(ai_response):
                    await update.message.reply_text(
                        f"🔊 **Voice Summary:**\n\n{voice_friendly_text}\n\n" +
                        "📖 *See the full detailed response above*\n\n" +
                        "*Educational support by Mraprguild's AI Assistant*"
                    )
            except Exception as e:
                logger.error(f"Error creating voice summary: {e}")
            
        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text("❌ Error processing voice message. Please try again.")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        try:
            user_text = update.message.text
            if not user_text:
                return
            
            # Check if it's a code snippet
            is_code = self._detect_code_in_message(user_text)
            
            if is_code:
                # Send thinking message
                thinking_msg = await update.message.reply_text("🔍 Analyzing your code...")
                
                # Analyze the code
                analysis_result = await self.code_analyzer.debug_code(user_text)
                await thinking_msg.edit_text(analysis_result, parse_mode=ParseMode.MARKDOWN)
            else:
                # Send thinking message
                thinking_msg = await update.message.reply_text("🤔 Thinking about your question...")
                
                # Get educational response
                ai_response = await self.gemini_assistant.get_educational_response(user_text, is_voice=False)
                await thinking_msg.edit_text(ai_response, parse_mode=ParseMode.MARKDOWN)
                
                # Add voice summary for accessibility
                try:
                    voice_friendly_text = self.voice_processor._prepare_educational_text(ai_response)
                    
                    if len(voice_friendly_text) < len(ai_response) and len(voice_friendly_text) > 50:
                        await update.message.reply_text(
                            f"🔊 **Voice Summary:**\n\n{voice_friendly_text}\n\n" +
                            "📖 *See the full detailed response above*\n\n" +
                            "*Educational support by Mraprguild's AI Assistant*"
                        )
                except Exception as e:
                    logger.error(f"Error creating voice summary for text: {e}")
                
        except Exception as e:
            logger.error(f"Error handling text message: {e}")
            await update.message.reply_text("❌ Error processing message. Please try again.")
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        try:
            document = update.message.document
            if not document:
                await update.message.reply_text("❌ No document found.")
                return
            
            # Check file extension
            filename = document.file_name or "unknown_file"
            file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
            
            # Supported code file extensions
            code_extensions = ['py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'php', 'go', 'rs', 'rb', 'ts', 'swift']
            
            if file_extension not in code_extensions:
                await update.message.reply_text(f"⚠️ File type '.{file_extension}' is not supported for code analysis. Please upload a code file.")
                return
            
            # Check file size (limit to 1MB)
            if document.file_size > 1024 * 1024:
                await update.message.reply_text("⚠️ File is too large. Please upload files smaller than 1MB.")
                return
            
            # Send processing message
            processing_msg = await update.message.reply_text(f"📁 Analyzing {filename}...")
            
            # Download and read file
            file = await document.get_file()
            
            with tempfile.NamedTemporaryFile(mode='w+b', suffix=f'.{file_extension}', delete=False) as temp_file:
                await file.download_to_drive(temp_file.name)
                
                # Read file content
                with open(temp_file.name, 'r', encoding='utf-8') as f:
                    file_content = f.read()
                
                # Clean up temp file
                os.unlink(temp_file.name)
            
            # Analyze file
            analysis_result = await self.code_analyzer.analyze_file(file_content, filename)
            await processing_msg.edit_text(analysis_result, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error handling document: {e}")
            await update.message.reply_text("❌ Error processing file. Please try again.")
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard callbacks"""
        try:
            query = update.callback_query
            await query.answer()
            
            data = query.data
            
            if data == 'voice_help':
                help_text = await self.educational_content.get_voice_help()
                await query.edit_message_text(help_text, parse_mode=ParseMode.MARKDOWN)
            
            elif data == 'tutorials':
                tutorials_text = await self.educational_content.get_tutorial_menu()
                await query.edit_message_text(tutorials_text, parse_mode=ParseMode.MARKDOWN)
            
            elif data == 'languages':
                languages_text = await self.educational_content.get_supported_languages()
                await query.edit_message_text(languages_text, parse_mode=ParseMode.MARKDOWN)
            
            elif data == 'debug_help':
                debug_help = await self.educational_content.get_debug_help()
                await query.edit_message_text(debug_help, parse_mode=ParseMode.MARKDOWN)
            
            elif data == 'review_help':
                review_help = await self.educational_content.get_review_help()
                await query.edit_message_text(review_help, parse_mode=ParseMode.MARKDOWN)
            
            elif data.startswith('tutorial_'):
                language = data.replace('tutorial_', '')
                tutorial_content = await self.educational_content.get_language_tutorial(language)
                await query.edit_message_text(tutorial_content, parse_mode=ParseMode.MARKDOWN)
            
            elif data.startswith('tutorials_'):
                category = data.replace('tutorials_', '')
                category_content = await self.educational_content.get_tutorial_category(category)
                await query.edit_message_text(category_content, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error handling callback: {e}")
            await query.edit_message_text("❌ Error processing request. Please try again.")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "🔧 **Technical Issue**\n\nSomething went wrong processing your request. Please try again or contact support.\n\n*Educational support by Mraprguild's AI Assistant*",
                parse_mode=ParseMode.MARKDOWN
            )
    
    def _detect_code_in_message(self, text: str) -> bool:
        """Detect if message contains code"""
        code_indicators = [
            r'def\s+\w+', r'function\s+\w+', r'class\s+\w+', r'import\s+\w+',
            r'#include', r'public\s+class', r'console\.log', r'print\s*\(',
            r'<\w+>', r'{\s*\w+:', r'SELECT\s+.*FROM'
        ]
        
        for pattern in code_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check for code-like structure
        lines = text.split('\n')
        if len(lines) > 3 and any(line.strip().startswith(('    ', '\t')) for line in lines):
            return True
        
        return False
    
    def run(self):
        """Start the bot"""
        logger.info("Educational Voice Assistant Bot starting...")
        self.app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
