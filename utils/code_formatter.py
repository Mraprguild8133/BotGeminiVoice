"""
Code formatting utilities for syntax highlighting and display
"""

import re
import logging
from typing import Dict, List, Optional
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name
from pygments.util import ClassNotFound

from .logger import setup_logger

logger = setup_logger(__name__)

class CodeFormatter:
    """Format and highlight code for educational display"""
    
    def __init__(self):
        # Language mappings for syntax highlighting
        self.language_mappings = {
            'python': 'python',
            'javascript': 'javascript',
            'js': 'javascript',
            'java': 'java',
            'cpp': 'cpp',
            'c++': 'cpp',
            'c': 'c',
            'html': 'html',
            'css': 'css',
            'php': 'php',
            'ruby': 'ruby',
            'go': 'go',
            'rust': 'rust',
            'swift': 'swift',
            'kotlin': 'kotlin',
            'scala': 'scala',
            'typescript': 'typescript',
            'ts': 'typescript',
            'sql': 'sql',
            'bash': 'bash',
            'shell': 'bash',
            'powershell': 'powershell'
        }
        
        # Common code patterns for detection
        self.code_patterns = [
            r'def\s+\w+\s*\(',  # Python function
            r'function\s+\w+\s*\(',  # JavaScript function
            r'class\s+\w+',  # Class definition
            r'import\s+\w+',  # Import statement
            r'#include\s*<',  # C/C++ include
            r'public\s+static\s+void\s+main',  # Java main
            r'console\.log\s*\(',  # JavaScript console.log
            r'print\s*\(',  # Python print
            r'System\.out\.print',  # Java print
            r'<\w+[^>]*>',  # HTML tags
            r'\w+\s*:\s*\w+\s*;',  # CSS properties
            r'SELECT\s+.*FROM\s+\w+',  # SQL query
            r'\$\w+',  # PHP/shell variables
            r'fn\s+\w+\s*\(',  # Rust function
            r'func\s+\w+\s*\(',  # Go function
        ]
    
    def format_code_in_text(self, text: str) -> str:
        """Format code blocks found in text"""
        # Pattern to match code blocks with optional language specification
        code_block_pattern = r'```(\w+)?\n(.*?)\n```'
        
        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)
            
            # Format the code block
            formatted_code = self._format_code_block(code, language)
            return f"```{language or ''}\n{formatted_code}\n```"
        
        # Replace code blocks
        formatted_text = re.sub(code_block_pattern, replace_code_block, text, flags=re.DOTALL)
        
        # Format inline code (single backticks)
        inline_code_pattern = r'`([^`]+)`'
        formatted_text = re.sub(inline_code_pattern, r'`\1`', formatted_text)
        
        return formatted_text
    
    def _format_code_block(self, code: str, language: Optional[str] = None) -> str:
        """Format a single code block with syntax highlighting"""
        try:
            # Clean up the code
            code = code.strip()
            
            if not code:
                return ""
            
            # Detect language if not provided
            if not language:
                language = self._detect_code_language(code)
            
            # Map language aliases
            if language and language.lower() in self.language_mappings:
                language = self.language_mappings[language.lower()]
            
            # Add educational comments if appropriate
            code_with_comments = self._add_educational_comments(code, language)
            
            return code_with_comments
            
        except Exception as e:
            logger.warning(f"Error formatting code block: {e}")
            return code
    
    def _detect_code_language(self, code: str) -> Optional[str]:
        """Detect programming language from code content"""
        code_lower = code.lower()
        
        # Language-specific patterns
        language_indicators = {
            'python': [
                r'def\s+\w+', r'import\s+\w+', r'from\s+\w+\s+import',
                r'print\s*\(', r'if\s+__name__\s*==', r':\s*$'
            ],
            'javascript': [
                r'function\s+\w+', r'var\s+\w+', r'let\s+\w+', r'const\s+\w+',
                r'console\.log', r'=>', r'document\.'
            ],
            'java': [
                r'public\s+class', r'public\s+static\s+void\s+main',
                r'System\.out\.print', r'import\s+java\.'
            ],
            'cpp': [
                r'#include\s*<', r'int\s+main\s*\(', r'std::',
                r'cout\s*<<', r'cin\s*>>', r'using\s+namespace'
            ],
            'c': [
                r'#include\s*<stdio\.h>', r'int\s+main\s*\(',
                r'printf\s*\(', r'scanf\s*\('
            ],
            'html': [
                r'<html', r'<head>', r'<body>', r'<div', r'<!DOCTYPE'
            ],
            'css': [
                r'[.#][\w-]+\s*{', r':\s*[\w-]+\s*;', r'@media', r'@import'
            ],
            'php': [
                r'<\?php', r'\$\w+', r'echo\s+', r'function\s+\w+'
            ],
            'sql': [
                r'SELECT\s+.*FROM', r'INSERT\s+INTO', r'UPDATE\s+\w+\s+SET',
                r'CREATE\s+TABLE'
            ]
        }
        
        # Score languages based on pattern matches
        language_scores = {}
        
        for language, patterns in language_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, code, re.IGNORECASE | re.MULTILINE))
                score += matches
            
            if score > 0:
                language_scores[language] = score
        
        # Return language with highest score
        if language_scores:
            detected = max(language_scores.keys(), key=lambda k: language_scores[k])
            logger.info(f"Detected language: {detected} (score: {language_scores[detected]})")
            return detected
        
        return None
    
    def _add_educational_comments(self, code: str, language: Optional[str]) -> str:
        """Add educational comments to code for learning purposes"""
        if not language:
            return code
        
        lines = code.split('\n')
        commented_lines = []
        
        for line in lines:
            # Add the original line
            commented_lines.append(line)
            
            # Add educational comments based on language and patterns
            if language == 'python':
                commented_lines.extend(self._add_python_comments(line))
            elif language == 'javascript':
                commented_lines.extend(self._add_javascript_comments(line))
            elif language == 'java':
                commented_lines.extend(self._add_java_comments(line))
        
        return '\n'.join(commented_lines)
    
    def _add_python_comments(self, line: str) -> List[str]:
        """Add Python-specific educational comments"""
        comments = []
        line_stripped = line.strip()
        
        # Function definition
        if re.match(r'def\s+\w+', line_stripped):
            comments.append("# Function definition - defines reusable code block")
        
        # Class definition
        elif re.match(r'class\s+\w+', line_stripped):
            comments.append("# Class definition - creates a blueprint for objects")
        
        # Import statement
        elif re.match(r'import\s+\w+|from\s+\w+', line_stripped):
            comments.append("# Import statement - brings external functionality")
        
        # List comprehension
        elif '[' in line and 'for' in line and 'in' in line:
            comments.append("# List comprehension - compact way to create lists")
        
        # Exception handling
        elif line_stripped.startswith('try:'):
            comments.append("# Try block - handles potential errors gracefully")
        elif line_stripped.startswith('except'):
            comments.append("# Exception handler - runs when errors occur")
        
        return comments
    
    def _add_javascript_comments(self, line: str) -> List[str]:
        """Add JavaScript-specific educational comments"""
        comments = []
        line_stripped = line.strip()
        
        # Function declaration
        if re.match(r'function\s+\w+', line_stripped):
            comments.append("// Function declaration - defines reusable code")
        
        # Arrow function
        elif '=>' in line:
            comments.append("// Arrow function - modern function syntax")
        
        # Variable declarations
        elif line_stripped.startswith('let '):
            comments.append("// let - block-scoped variable declaration")
        elif line_stripped.startswith('const '):
            comments.append("// const - constant variable declaration")
        elif line_stripped.startswith('var '):
            comments.append("// var - function-scoped variable declaration")
        
        # DOM manipulation
        elif 'document.' in line:
            comments.append("// DOM manipulation - interacting with webpage elements")
        
        return comments
    
    def _add_java_comments(self, line: str) -> List[str]:
        """Add Java-specific educational comments"""
        comments = []
        line_stripped = line.strip()
        
        # Class declaration
        if re.match(r'public\s+class', line_stripped):
            comments.append("// Public class - accessible from other packages")
        
        # Main method
        elif 'public static void main' in line:
            comments.append("// Main method - program entry point")
        
        # Access modifiers
        elif line_stripped.startswith('private '):
            comments.append("// Private - only accessible within this class")
        elif line_stripped.startswith('protected '):
            comments.append("// Protected - accessible in package and subclasses")
        
        return comments
    
    def extract_code_blocks(self, text: str) -> List[Dict]:
        """Extract all code blocks from text with metadata"""
        code_blocks = []
        
        # Pattern for fenced code blocks
        pattern = r'```(\w+)?\n(.*?)\n```'
        
        for match in re.finditer(pattern, text, re.DOTALL):
            language = match.group(1)
            code = match.group(2).strip()
            
            if code:  # Only include non-empty blocks
                code_blocks.append({
                    'language': language or self._detect_code_language(code),
                    'code': code,
                    'start_pos': match.start(),
                    'end_pos': match.end()
                })
        
        return code_blocks
    
    def create_code_snippet_explanation(self, code: str, language: Optional[str] = None) -> str:
        """Create an educational explanation of a code snippet"""
        explanation = "🔍 **Code Analysis:**\n\n"
        
        if not language:
            language = self._detect_code_language(code)
        
        if language:
            explanation += f"**Language:** {language.title()}\n\n"
        
        # Analyze code structure
        lines = code.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        
        explanation += f"**Structure Analysis:**\n"
        explanation += f"• Total lines: {len(lines)}\n"
        explanation += f"• Code lines: {len(non_empty_lines)}\n"
        
        # Identify key components
        components = self._identify_code_components(code, language)
        if components:
            explanation += f"\n**Key Components:**\n"
            for component in components:
                explanation += f"• {component}\n"
        
        # Add educational insights
        insights = self._generate_code_insights(code, language)
        if insights:
            explanation += f"\n**Educational Insights:**\n"
            for insight in insights:
                explanation += f"💡 {insight}\n"
        
        return explanation
    
    def _identify_code_components(self, code: str, language: Optional[str]) -> List[str]:
        """Identify key components in code"""
        components = []
        
        if not language:
            return components
        
        # Common patterns across languages
        if re.search(r'def\s+\w+|function\s+\w+|func\s+\w+', code, re.IGNORECASE):
            components.append("Functions - Reusable code blocks")
        
        if re.search(r'class\s+\w+', code, re.IGNORECASE):
            components.append("Classes - Object-oriented programming structures")
        
        if re.search(r'if\s+.*:', code, re.IGNORECASE):
            components.append("Conditional statements - Decision making logic")
        
        if re.search(r'for\s+.*:|while\s+.*:', code, re.IGNORECASE):
            components.append("Loops - Repetitive execution structures")
        
        if re.search(r'import\s+|#include\s+|require\s*\(', code, re.IGNORECASE):
            components.append("Dependencies - External code/libraries")
        
        if re.search(r'try\s*{|try:', code, re.IGNORECASE):
            components.append("Error handling - Exception management")
        
        return components
    
    def _generate_code_insights(self, code: str, language: Optional[str]) -> List[str]:
        """Generate educational insights about code"""
        insights = []
        
        # General insights
        if len(code.split('\n')) > 50:
            insights.append("This is a substantial piece of code - consider breaking it into smaller functions")
        
        # Count complexity indicators
        complexity_indicators = len(re.findall(r'if\s+|for\s+|while\s+|switch\s+', code, re.IGNORECASE))
        if complexity_indicators > 10:
            insights.append("High complexity detected - consider simplifying or adding comments")
        
        # Check for comments
        has_comments = bool(re.search(r'#.*|//.*|/\*.*\*/', code, re.DOTALL))
        if not has_comments and len(code) > 100:
            insights.append("Consider adding comments to explain complex logic")
        
        # Language-specific insights
        if language == 'python':
            if 'print(' in code:
                insights.append("Using print() for output - great for debugging and user feedback")
            if 'def ' in code:
                insights.append("Function definitions help organize code into reusable components")
        
        elif language == 'javascript':
            if 'console.log' in code:
                insights.append("console.log() is excellent for debugging and monitoring values")
            if '=>' in code:
                insights.append("Arrow functions provide concise syntax for function expressions")
        
        return insights
