#!/usr/bin/env python3
"""
Educational Telegram Voice Assistant Bot powered by Gemini AI
Created by Mraprguild - For coding support and programming education
"""

import os
import asyncio
import logging
from dotenv import load_dotenv
from bot.telegram_bot import TelegramBot

# Load environment variables
load_dotenv()

def main():
    """Main entry point for the Telegram bot"""
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    
    # Validate required environment variables
    bot_token = os.getenv("BOT_TOKEN")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not bot_token:
        logger.error("BOT_TOKEN environment variable is required!")
        logger.error("Please set your Telegram bot token from @BotFather")
        return
        
    if not gemini_api_key:
        logger.error("GEMINI_API_KEY environment variable is required!")
        logger.error("Please set your Google Gemini API key")
        return
    
    # Initialize and run the bot
    bot = TelegramBot(bot_token)
    logger.info("Starting Educational Telegram Voice Assistant Bot by Mraprguild...")
    
    try:
        # Run the bot
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed with error: {e}")
    finally:
        logger.info("Bot shutdown complete")

if __name__ == "__main__":
    main()
