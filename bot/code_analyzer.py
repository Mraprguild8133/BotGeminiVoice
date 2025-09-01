"""
Code analysis module for debugging, review, and educational feedback
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from google import genai
from google.genai import types
import os

from utils.logger import setup_logger
from utils.code_formatter import CodeFormatter

logger = setup_logger(__name__)

class CodeAnalyzer:
    """Analyze code for debugging, review, and educational purposes"""
    
    def __init__(self):
        # Initialize Gemini client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.code_formatter = CodeFormatter()
        
        # Language detection patterns
        self.language_patterns = {
            'python': [r'def\s+\w+', r'import\s+\w+', r'class\s+\w+', r'print\s*\(', r'if\s+__name__\s*==\s*[\'"]__main__[\'"]'],
            'javascript': [r'function\s+\w+', r'var\s+\w+', r'let\s+\w+', r'const\s+\w+', r'console\.log', r'=>'],
            'java': [r'public\s+class', r'public\s+static\s+void\s+main', r'System\.out\.print', r'import\s+java\.'],
            'cpp': [r'#include\s*<', r'int\s+main\s*\(', r'std::', r'cout\s*<<', r'cin\s*>>'],
            'c': [r'#include\s*<', r'int\s+main\s*\(', r'printf\s*\(', r'scanf\s*\('],
            'html': [r'<html', r'<head>', r'<body>', r'<div', r'<!DOCTYPE'],
            'css': [r'[.#][\w-]+\s*{', r':\s*[\w-]+\s*;', r'@media', r'@import'],
            'php': [r'<\?php', r'\$\w+', r'function\s+\w+', r'echo\s+'],
            'go': [r'package\s+main', r'func\s+main\s*\(', r'import\s*\(', r'fmt\.Print'],
            'rust': [r'fn\s+main\s*\(', r'let\s+\w+', r'println!\s*\(', r'use\s+std::']
        }
    
    async def debug_code(self, code: str) -> str:
        """Debug code and provide educational explanations"""
        try:
            # Detect programming language
            detected_language = self._detect_language(code)
            
            # Analyze code for common issues
            issues = self._analyze_syntax_issues(code, detected_language)
            
            # Get AI-powered debugging assistance
            debug_prompt = f"""
            As an educational coding tutor, help debug this {detected_language or 'code'}.
            
            Code to debug:
            ```{detected_language or ''}
            {code}
            ```
            
            Please provide:
            1. Identification of any errors or issues
            2. Clear explanation of what's wrong and why
            3. Step-by-step solution with corrected code
            4. Educational explanation of the concepts involved
            5. Tips to avoid similar mistakes in the future
            
            Focus on teaching the user, not just fixing the code.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=debug_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Lower temperature for more precise debugging
                    max_output_tokens=2048
                )
            )
            
            # Format the debugging response
            formatted_response = self._format_debug_response(
                response.text if response.text else "",
                detected_language,
                issues
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error debugging code: {e}")
            return self._get_debug_fallback_response()
    
    async def review_code(self, code: str) -> str:
        """Review code and provide educational feedback"""
        try:
            # Detect programming language
            detected_language = self._detect_language(code)
            
            # Analyze code quality metrics
            quality_metrics = self._analyze_code_quality(code, detected_language)
            
            # Get AI-powered code review
            review_prompt = f"""
            As an experienced programming tutor, provide an educational code review for this {detected_language or 'code'}.
            
            Code to review:
            ```{detected_language or ''}
            {code}
            ```
            
            Please provide:
            1. Overall code quality assessment
            2. Best practices analysis
            3. Performance and efficiency considerations
            4. Readability and maintainability feedback
            5. Security considerations (if applicable)
            6. Specific improvement suggestions with examples
            7. Educational insights about the code patterns used
            
            Focus on helping the user learn better coding practices.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=review_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.4,
                    max_output_tokens=2048
                )
            )
            
            # Format the review response
            formatted_response = self._format_review_response(
                response.text if response.text else "",
                detected_language,
                quality_metrics
            )
            
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error reviewing code: {e}")
            return self._get_review_fallback_response()
    
    async def analyze_file(self, file_content: str, filename: str) -> str:
        """Analyze uploaded code file"""
        try:
            # Extract language from filename
            file_extension = filename.split('.')[-1].lower() if '.' in filename else ''
            language_map = {
                'py': 'python', 'js': 'javascript', 'java': 'java',
                'cpp': 'cpp', 'c': 'c', 'html': 'html', 'css': 'css',
                'php': 'php', 'go': 'go', 'rs': 'rust', 'rb': 'ruby'
            }
            
            detected_language = language_map.get(file_extension, self._detect_language(file_content))
            
            # Comprehensive file analysis
            analysis_prompt = f"""
            As an educational coding tutor, provide a comprehensive analysis of this {detected_language or 'code'} file.
            
            Filename: {filename}
            File content:
            ```{detected_language or ''}
            {file_content}
            ```
            
            Please provide:
            1. File structure and organization analysis
            2. Code functionality overview
            3. Error detection and debugging suggestions
            4. Code quality and best practices review
            5. Performance optimization opportunities
            6. Educational insights about the code architecture
            7. Suggestions for improvement with examples
            
            Make this analysis educational and helpful for learning.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=analysis_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    max_output_tokens=3072
                )
            )
            
            return self._format_file_analysis_response(
                response.text if response.text else "",
                filename,
                detected_language
            )
            
        except Exception as e:
            logger.error(f"Error analyzing file: {e}")
            return self._get_analysis_fallback_response(filename)
    
    def _detect_language(self, code: str) -> Optional[str]:
        """Detect programming language from code patterns"""
        code_lower = code.lower()
        
        # Score each language based on pattern matches
        language_scores = {}
        
        for language, patterns in self.language_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.IGNORECASE))
                score += matches
            
            if score > 0:
                language_scores[language] = score
        
        # Return language with highest score
        if language_scores:
            return max(language_scores.keys(), key=lambda k: language_scores[k])
        
        return None
    
    def _analyze_syntax_issues(self, code: str, language: Optional[str]) -> List[Dict]:
        """Analyze code for common syntax issues"""
        issues = []
        
        # Common issues across languages
        if language == 'python':
            issues.extend(self._analyze_python_issues(code))
        elif language == 'javascript':
            issues.extend(self._analyze_javascript_issues(code))
        elif language in ['java', 'cpp', 'c']:
            issues.extend(self._analyze_c_family_issues(code))
        
        return issues
    
    def _analyze_python_issues(self, code: str) -> List[Dict]:
        """Analyze Python-specific issues"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for common Python issues
            if re.search(r'if\s+.*=\s+', line):  # Assignment instead of comparison
                issues.append({
                    'line': i,
                    'type': 'syntax',
                    'message': 'Possible assignment (=) instead of comparison (==)',
                    'severity': 'error'
                })
            
            if re.search(r'print\s+[^(]', line):  # Python 2 print syntax
                issues.append({
                    'line': i,
                    'type': 'syntax',
                    'message': 'Use print() function syntax for Python 3',
                    'severity': 'warning'
                })
        
        return issues
    
    def _analyze_javascript_issues(self, code: str) -> List[Dict]:
        """Analyze JavaScript-specific issues"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if '==' in line and '===' not in line:
                issues.append({
                    'line': i,
                    'type': 'best_practice',
                    'message': 'Consider using strict equality (===) instead of ==',
                    'severity': 'warning'
                })
        
        return issues
    
    def _analyze_c_family_issues(self, code: str) -> List[Dict]:
        """Analyze C/C++/Java issues"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            if re.search(r'if\s*\([^)]*=[^=]', line):  # Assignment in condition
                issues.append({
                    'line': i,
                    'type': 'syntax',
                    'message': 'Possible assignment in conditional (use == for comparison)',
                    'severity': 'error'
                })
        
        return issues
    
    def _analyze_code_quality(self, code: str, language: Optional[str]) -> Dict:
        """Analyze code quality metrics"""
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        metrics = {
            'total_lines': len(lines),
            'code_lines': len(non_empty_lines),
            'complexity': self._calculate_complexity(code),
            'readability': self._assess_readability(code),
            'language': language
        }
        
        return metrics
    
    def _calculate_complexity(self, code: str) -> str:
        """Calculate approximate code complexity"""
        # Count control structures as complexity indicators
        complexity_patterns = [
            r'\bif\b', r'\bfor\b', r'\bwhile\b', r'\bswitch\b',
            r'\btry\b', r'\bcatch\b', r'\belse\b'
        ]
        
        complexity_count = 0
        for pattern in complexity_patterns:
            complexity_count += len(re.findall(pattern, code, re.IGNORECASE))
        
        if complexity_count <= 5:
            return 'Low'
        elif complexity_count <= 15:
            return 'Medium'
        else:
            return 'High'
    
    def _assess_readability(self, code: str) -> str:
        """Assess code readability"""
        # Simple readability assessment based on various factors
        lines = code.split('\n')
        
        # Factors that improve readability
        has_comments = any('//' in line or '#' in line or '/*' in line for line in lines)
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        has_whitespace = any(line.strip() == '' for line in lines)
        
        # Score based on factors
        score = 0
        if has_comments:
            score += 1
        if avg_line_length < 80:  # Reasonable line length
            score += 1
        if has_whitespace:  # Has spacing between sections
            score += 1
        
        if score >= 2:
            return 'Good'
        elif score == 1:
            return 'Fair'
        else:
            return 'Needs Improvement'
    
    def _format_debug_response(self, ai_response: str, language: Optional[str], issues: List[Dict]) -> str:
        """Format debugging response"""
        response = "🐛 **Code Debugging Analysis**\n\n"
        
        if language:
            response += f"**Detected Language:** {language.title()}\n\n"
        
        # Add detected issues if any
        if issues:
            response += "**Quick Issue Detection:**\n"
            for issue in issues[:3]:  # Show top 3 issues
                response += f"• Line {issue['line']}: {issue['message']} ({issue['severity']})\n"
            response += "\n"
        
        # Add AI analysis
        response += "**Detailed Analysis:**\n"
        response += self.code_formatter.format_code_in_text(ai_response)
        
        response += "\n\n💡 **Learning Tip:** Understanding errors is key to becoming a better programmer!"
        response += "\n\n---\n*Debug assistance by Mraprguild's AI Assistant* 🔧"
        
        return response
    
    def _format_review_response(self, ai_response: str, language: Optional[str], metrics: Dict) -> str:
        """Format code review response"""
        response = "📝 **Code Review Analysis**\n\n"
        
        if language:
            response += f"**Language:** {language.title()}\n"
        
        response += f"**Code Metrics:**\n"
        response += f"• Total Lines: {metrics.get('total_lines', 'N/A')}\n"
        response += f"• Code Lines: {metrics.get('code_lines', 'N/A')}\n"
        response += f"• Complexity: {metrics.get('complexity', 'N/A')}\n"
        response += f"• Readability: {metrics.get('readability', 'N/A')}\n\n"
        
        # Add AI analysis
        response += "**Detailed Review:**\n"
        response += self.code_formatter.format_code_in_text(ai_response)
        
        response += "\n\n🏆 **Remember:** Great code is not just working code, but code that others can understand and maintain!"
        response += "\n\n---\n*Code review by Mraprguild's AI Assistant* ⭐"
        
        return response
    
    def _format_file_analysis_response(self, ai_response: str, filename: str, language: Optional[str]) -> str:
        """Format file analysis response"""
        response = f"📁 **File Analysis: {filename}**\n\n"
        
        if language:
            response += f"**Detected Language:** {language.title()}\n\n"
        
        response += "**Comprehensive Analysis:**\n"
        response += self.code_formatter.format_code_in_text(ai_response)
        
        response += "\n\n📚 **File Analysis Complete!** Use this feedback to improve your code quality and structure."
        response += "\n\n---\n*File analysis by Mraprguild's AI Assistant* 📊"
        
        return response
    
    def _get_debug_fallback_response(self) -> str:
        """Fallback response for debugging"""
        return """
🐛 **Code Debugging Assistant**

I'm here to help you debug your code! To get the best debugging assistance:

**For better results:**
1. Share your complete code snippet
2. Include any error messages you're seeing
3. Describe what you expected vs what's happening
4. Mention which programming language you're using

**Common debugging steps:**
1. Check syntax carefully (brackets, semicolons, indentation)
2. Look for typos in variable names
3. Verify logic flow with print statements/console.log
4. Check data types and variable scope

Try sharing your code again, and I'll provide detailed debugging help!

*Debug assistance by Mraprguild's AI Assistant* 🔧
        """
    
    def _get_review_fallback_response(self) -> str:
        """Fallback response for code review"""
        return """
📝 **Code Review Assistant**

I'm ready to review your code and help you improve it! For a comprehensive review:

**Share your code with:**
1. Complete code snippets or files
2. Context about what the code should do
3. Any specific concerns you have
4. The programming language you're using

**My review will cover:**
• Code quality and best practices
• Performance optimization opportunities
• Readability and maintainability
• Security considerations
• Educational insights and improvements

Ready to make your code even better? Share it with me!

*Code review by Mraprguild's AI Assistant* ⭐
        """
    
    def _get_analysis_fallback_response(self, filename: str) -> str:
        """Fallback response for file analysis"""
        return f"""
📁 **File Analysis: {filename}**

I encountered an issue analyzing your file, but I'm here to help! 

**For successful file analysis:**
1. Ensure the file contains readable code
2. Use common programming language extensions
3. Check that the file isn't corrupted
4. Try uploading again

**I can analyze files in:**
• Python (.py)
• JavaScript (.js) 
• Java (.java)
• C/C++ (.c, .cpp)
• HTML (.html)
• CSS (.css)
• And many more!

Please try uploading your file again, and I'll provide comprehensive analysis!

*File analysis by Mraprguild's AI Assistant* 📊
        """
