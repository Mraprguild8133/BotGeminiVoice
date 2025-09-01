"""
Gemini AI assistant for educational coding support
"""

import os
import logging
from typing import Optional
from google import genai
from google.genai import types

from utils.logger import setup_logger
from utils.code_formatter import CodeFormatter

logger = setup_logger(__name__)

class GeminiAssistant:
    """Gemini AI assistant focused on educational programming support"""
    
    def __init__(self):
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.code_formatter = CodeFormatter()
        
        # Educational system prompt
        self.system_prompt = """You are an experienced programming tutor and educational coding assistant created by Mraprguild. 

Your role is to:
1. Provide clear, step-by-step explanations suitable for learners
2. Break down complex concepts into digestible parts
3. Use examples and analogies to help understanding
4. Identify common mistakes and explain how to avoid them
5. Encourage good coding practices and best practices
6. Be patient and supportive in your teaching approach

When helping with code:
- Always explain the reasoning behind solutions
- Point out potential issues and improvements
- Provide educational context for your suggestions
- Use simple language while being technically accurate
- Include examples when helpful

Focus on teaching and learning, not just providing answers. Help users understand the 'why' behind the 'what'.
"""
    
    async def get_educational_response(self, user_message: str, is_voice: bool = False) -> str:
        """Get educational response from Gemini AI"""
        try:
            # Prepare the prompt with educational context
            educational_prompt = self._prepare_educational_prompt(user_message, is_voice)
            
            # Generate response using Gemini
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=educational_prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.7,  # Balanced creativity for educational content
                    max_output_tokens=2048
                )
            )
            
            if response and response.text:
                formatted_response = self._format_educational_response(response.text, is_voice)
                return formatted_response
            else:
                return self._get_fallback_response()
                
        except Exception as e:
            logger.error(f"Error getting Gemini response: {e}")
            return self._get_error_response()
    
    async def explain_concept(self, concept: str, programming_language: Optional[str] = None) -> str:
        """Explain a programming concept in educational terms"""
        try:
            prompt = f"""
            Explain the programming concept '{concept}' in an educational, beginner-friendly way.
            {f"Focus on {programming_language} specifically." if programming_language else ""}
            
            Please include:
            1. A simple definition
            2. Why it's important/useful
            3. A basic example with explanation
            4. Common use cases
            5. Common mistakes to avoid
            
            Make it engaging and easy to understand for learners.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.6
                )
            )
            
            return self._format_educational_response(response.text if response.text else "")
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return f"I apologize, but I couldn't generate an explanation for '{concept}' right now. Please try again or ask about a specific aspect you'd like to understand."
    
    async def provide_learning_path(self, topic: str) -> str:
        """Provide a structured learning path for a topic"""
        try:
            prompt = f"""
            Create a structured learning path for '{topic}' suitable for beginners to intermediate learners.
            
            Include:
            1. Prerequisites (what to know first)
            2. Step-by-step learning sequence
            3. Key concepts to master at each step
            4. Practical exercises or projects
            5. Resources for further learning
            
            Make it actionable and encouraging.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_prompt,
                    temperature=0.5
                )
            )
            
            return self._format_educational_response(response.text if response.text else "")
            
        except Exception as e:
            logger.error(f"Error creating learning path: {e}")
            return f"I couldn't create a learning path for '{topic}' right now. Please try asking about specific aspects you'd like to learn."
    
    def _prepare_educational_prompt(self, user_message: str, is_voice: bool) -> str:
        """Prepare user message with educational context"""
        voice_context = " (This question came from a voice message, so provide a clear, spoken-friendly explanation.)" if is_voice else ""
        
        educational_context = f"""
        Educational Context: The user is learning programming and needs help understanding concepts or solving problems.
        Please provide a teaching-focused response that helps them learn, not just get answers.{voice_context}
        
        User Question: {user_message}
        
        Please respond in a helpful, educational manner with:
        1. Clear explanations
        2. Step-by-step breakdowns when appropriate
        3. Examples and analogies
        4. Best practices guidance
        5. Encouragement and learning tips
        """
        
        return educational_context
    
    def _format_educational_response(self, response: str, is_voice: bool = False) -> str:
        """Format response for educational delivery"""
        if not response:
            return self._get_fallback_response()
        
        # Add educational header
        formatted_response = "🎓 **Educational Assistant Response:**\n\n"
        
        # Format code blocks if present
        formatted_response += self.code_formatter.format_code_in_text(response)
        
        # Add learning encouragement footer
        if not is_voice:
            formatted_response += "\n\n💡 **Remember:** Practice makes perfect! Try implementing this concept in your own code."
            formatted_response += "\n\n🤔 **Need clarification?** Feel free to ask follow-up questions about any part!"
        
        # Add creator signature
        formatted_response += "\n\n---\n*Educational support by Mraprguild's AI Assistant* 🚀"
        
        return formatted_response
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when AI fails"""
        return """
🎓 **I'm here to help with your coding questions!**

I can assist you with:
• Programming concepts and explanations
• Code debugging and error fixing
• Best practices and code review
• Step-by-step problem solving
• Learning paths for different technologies

Please try rephrasing your question or ask about a specific programming topic, and I'll do my best to provide a clear, educational explanation!

*Educational support by Mraprguild's AI Assistant* 🚀
        """
    
    def _get_error_response(self) -> str:
        """Get error response when something goes wrong"""
        return """
🔧 **Technical Issue**

I'm experiencing a temporary issue with my AI processing. Please:
1. Try asking your question again
2. Make sure your question is clear and specific
3. Check your internet connection

If the problem persists, the issue might be on our end and should resolve shortly.

*Educational support by Mraprguild's AI Assistant* 🚀
        """
