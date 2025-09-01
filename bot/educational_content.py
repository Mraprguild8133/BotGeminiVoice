"""
Educational content provider for programming tutorials and help
"""

import logging
from typing import Dict, List
from utils.logger import setup_logger

logger = setup_logger(__name__)

class EducationalContent:
    """Provide educational programming content and tutorials"""
    
    def __init__(self):
        self.supported_languages = {
            'python': {
                'name': 'Python',
                'description': 'Beginner-friendly, versatile programming language',
                'use_cases': ['Web development', 'Data science', 'AI/ML', 'Automation'],
                'difficulty': 'Beginner'
            },
            'javascript': {
                'name': 'JavaScript',
                'description': 'Essential language for web development',
                'use_cases': ['Web frontend', 'Node.js backend', 'Mobile apps'],
                'difficulty': 'Beginner-Intermediate'
            },
            'java': {
                'name': 'Java',
                'description': 'Object-oriented language for enterprise applications',
                'use_cases': ['Enterprise software', 'Android development', 'Web backends'],
                'difficulty': 'Intermediate'
            },
            'cpp': {
                'name': 'C++',
                'description': 'High-performance systems programming language',
                'use_cases': ['System programming', 'Game development', 'Embedded systems'],
                'difficulty': 'Advanced'
            },
            'html': {
                'name': 'HTML',
                'description': 'Markup language for web structure',
                'use_cases': ['Web development', 'Email templates', 'Documentation'],
                'difficulty': 'Beginner'
            },
            'css': {
                'name': 'CSS',
                'description': 'Styling language for web presentation',
                'use_cases': ['Web styling', 'Responsive design', 'Animations'],
                'difficulty': 'Beginner'
            },
            'react': {
                'name': 'React',
                'description': 'JavaScript library for user interfaces',
                'use_cases': ['Web applications', 'Single-page apps', 'Mobile apps'],
                'difficulty': 'Intermediate'
            }
        }
        
        self.tutorial_categories = {
            'beginner': {
                'title': 'Beginner Programming Basics',
                'topics': [
                    'Variables and Data Types',
                    'Control Structures (if/else, loops)',
                    'Functions and Methods',
                    'Basic Input/Output',
                    'Error Handling Basics'
                ]
            },
            'ds': {
                'title': 'Data Structures',
                'topics': [
                    'Arrays and Lists',
                    'Stacks and Queues',
                    'Linked Lists',
                    'Trees and Graphs',
                    'Hash Tables/Dictionaries'
                ]
            },
            'algo': {
                'title': 'Algorithms',
                'topics': [
                    'Sorting Algorithms',
                    'Searching Algorithms',
                    'Recursion',
                    'Dynamic Programming',
                    'Graph Algorithms'
                ]
            },
            'web': {
                'title': 'Web Development',
                'topics': [
                    'HTML Structure',
                    'CSS Styling',
                    'JavaScript Basics',
                    'Responsive Design',
                    'Frontend Frameworks'
                ]
            },
            'debug': {
                'title': 'Debugging Techniques',
                'topics': [
                    'Reading Error Messages',
                    'Using Debuggers',
                    'Print/Log Debugging',
                    'Common Bug Patterns',
                    'Testing Strategies'
                ]
            }
        }
    
    async def get_supported_languages(self) -> str:
        """Get formatted list of supported programming languages"""
        response = "🔍 **Supported Programming Languages**\n\n"
        
        for lang_key, lang_info in self.supported_languages.items():
            response += f"**{lang_info['name']}** ({lang_info['difficulty']})\n"
            response += f"• {lang_info['description']}\n"
            response += f"• Use cases: {', '.join(lang_info['use_cases'])}\n\n"
        
        response += "💡 **Don't see your language?** I can still help! Just mention the language in your question.\n\n"
        response += "🎯 **How to get help:**\n"
        response += "• Ask questions about any of these languages\n"
        response += "• Share code for review or debugging\n"
        response += "• Request concept explanations\n"
        response += "• Get learning roadmaps and tutorials\n\n"
        
        response += "*Language support by Mraprguild's AI Assistant* 🚀"
        
        return response
    
    async def get_tutorial_menu(self) -> str:
        """Get tutorial category menu"""
        response = "📚 **Programming Tutorials & Learning Paths**\n\n"
        response += "Choose a category to explore learning materials:\n\n"
        
        for cat_key, cat_info in self.tutorial_categories.items():
            response += f"**{cat_info['title']}**\n"
            response += f"Topics: {', '.join(cat_info['topics'][:3])}...\n\n"
        
        response += "🎓 **How tutorials work:**\n"
        response += "• Step-by-step explanations\n"
        response += "• Code examples with comments\n"
        response += "• Practice exercises\n"
        response += "• Common mistakes to avoid\n\n"
        
        response += "📝 **Interactive learning:** Ask me to explain any concept in detail!\n\n"
        response += "*Educational content by Mraprguild's AI Assistant* 📖"
        
        return response
    
    async def get_voice_help(self) -> str:
        """Get voice assistance help"""
        response = "🎤 **Voice Assistant Help**\n\n"
        
        response += "**How to use voice messages:**\n"
        response += "1. **Record clearly** - Speak close to your device microphone\n"
        response += "2. **Speak slowly** - This helps with accurate transcription\n"
        response += "3. **Be specific** - State your programming language and question clearly\n"
        response += "4. **Keep it focused** - One question per voice message works best\n\n"
        
        response += "**Great voice questions:**\n"
        response += "• \"Explain what recursion is in Python\"\n"
        response += "• \"How do I fix a syntax error in JavaScript?\"\n"
        response += "• \"What are the basics of object-oriented programming?\"\n"
        response += "• \"Walk me through debugging steps\"\n\n"
        
        response += "**Voice response features:**\n"
        response += "• I'll show you what I understood from your voice\n"
        response += "• You'll get detailed text explanations\n"
        response += "• For concepts, I can provide audio explanations too!\n\n"
        
        response += "🎯 **Pro tip:** If voice recognition isn't working well, try typing your question - I'm equally helpful with text!\n\n"
        
        response += "*Voice assistance by Mraprguild's AI Assistant* 🔊"
        
        return response
    
    async def get_debug_help(self) -> str:
        """Get debugging assistance help"""
        response = "🐛 **Debugging Help Guide**\n\n"
        
        response += "**How I can help debug your code:**\n"
        response += "1. **Error Analysis** - Send error messages for explanation\n"
        response += "2. **Code Review** - Share code that's not working as expected\n"
        response += "3. **Logic Issues** - Describe unexpected behavior\n"
        response += "4. **Performance Problems** - Code running slowly or inefficiently\n\n"
        
        response += "**Debugging process:**\n"
        response += "• **Identify** the problem and error type\n"
        response += "• **Explain** why the error occurred\n"
        response += "• **Provide** step-by-step solution\n"
        response += "• **Teach** how to avoid similar issues\n"
        response += "• **Suggest** best practices\n\n"
        
        response += "**What to include in your debug request:**\n"
        response += "• Your complete code snippet\n"
        response += "• Any error messages you're seeing\n"
        response += "• What you expected to happen\n"
        response += "• What actually happened\n"
        response += "• Programming language you're using\n\n"
        
        response += "🎯 **Example:** \"My Python function isn't returning the right value\" + code\n\n"
        
        response += "*Debug assistance by Mraprguild's AI Assistant* 🔧"
        
        return response
    
    async def get_review_help(self) -> str:
        """Get code review help"""
        response = "📝 **Code Review Help Guide**\n\n"
        
        response += "**What my code review includes:**\n"
        response += "• **Quality Assessment** - Overall code structure and style\n"
        response += "• **Best Practices** - Industry-standard coding conventions\n"
        response += "• **Performance** - Efficiency and optimization opportunities\n"
        response += "• **Security** - Potential vulnerabilities and fixes\n"
        response += "• **Readability** - Code clarity and maintainability\n"
        response += "• **Educational Insights** - Learning opportunities\n\n"
        
        response += "**How to request a review:**\n"
        response += "1. Share your complete code (functions, classes, or full programs)\n"
        response += "2. Mention the programming language\n"
        response += "3. Describe what the code is supposed to do\n"
        response += "4. Ask specific questions if you have concerns\n\n"
        
        response += "**Review focus areas:**\n"
        response += "✅ **Working code** - Make good code even better\n"
        response += "🔍 **Learning** - Understand why changes are suggested\n"
        response += "⚡ **Performance** - Make code faster and more efficient\n"
        response += "📖 **Readability** - Code that others can understand\n\n"
        
        response += "💡 **Remember:** Code reviews are about learning and improvement, not criticism!\n\n"
        
        response += "*Code review by Mraprguild's AI Assistant* ⭐"
        
        return response
    
    async def get_language_tutorial(self, language: str) -> str:
        """Get tutorial for specific language"""
        if language not in self.supported_languages:
            return f"📚 Tutorial for {language.title()} coming soon! In the meantime, ask me specific questions about {language} and I'll be happy to help."
        
        lang_info = self.supported_languages[language]
        
        response = f"📚 **{lang_info['name']} Learning Guide**\n\n"
        response += f"**About {lang_info['name']}:**\n"
        response += f"{lang_info['description']}\n"
        response += f"Difficulty Level: {lang_info['difficulty']}\n\n"
        
        response += f"**What you can build:**\n"
        for use_case in lang_info['use_cases']:
            response += f"• {use_case}\n"
        response += "\n"
        
        # Add language-specific learning path
        if language == 'python':
            response += self._get_python_tutorial()
        elif language == 'javascript':
            response += self._get_javascript_tutorial()
        elif language == 'java':
            response += self._get_java_tutorial()
        elif language == 'cpp':
            response += self._get_cpp_tutorial()
        elif language == 'react':
            response += self._get_react_tutorial()
        else:
            response += "**Learning Path:**\n"
            response += "1. Basic syntax and structure\n"
            response += "2. Variables and data types\n"
            response += "3. Control structures\n"
            response += "4. Functions and methods\n"
            response += "5. Object-oriented concepts (if applicable)\n"
            response += "6. Libraries and frameworks\n"
            response += "7. Best practices and patterns\n\n"
        
        response += "🎯 **Ready to start?** Ask me specific questions about any topic above!\n\n"
        response += "*Tutorial by Mraprguild's AI Assistant* 📖"
        
        return response
    
    async def get_tutorial_category(self, category: str) -> str:
        """Get tutorial content for specific category"""
        if category not in self.tutorial_categories:
            return "📚 Tutorial category not found. Please try one of the available categories."
        
        cat_info = self.tutorial_categories[category]
        
        response = f"📚 **{cat_info['title']} Tutorial**\n\n"
        
        if category == 'beginner':
            response += self._get_beginner_tutorial()
        elif category == 'ds':
            response += self._get_data_structures_tutorial()
        elif category == 'algo':
            response += self._get_algorithms_tutorial()
        elif category == 'web':
            response += self._get_web_development_tutorial()
        elif category == 'debug':
            response += self._get_debugging_tutorial()
        
        response += "\n\n💡 **Interactive Learning:** Ask me to explain any of these concepts in detail with examples!\n\n"
        response += "*Tutorial by Mraprguild's AI Assistant* 📖"
        
        return response
    
    def _get_python_tutorial(self) -> str:
        """Python-specific tutorial content"""
        return """**Python Learning Path:**

**1. Python Basics (Week 1-2)**
• Variables and data types (int, str, list, dict)
• Input/output with input() and print()
• Indentation and code structure

**2. Control Flow (Week 2-3)**
• if/elif/else statements
• for and while loops
• break and continue

**3. Functions and Modules (Week 3-4)**
• Defining functions with def
• Parameters and return values
• Importing modules and packages

**4. Data Structures (Week 4-5)**
• Lists, tuples, dictionaries, sets
• List comprehensions
• File handling

**5. Object-Oriented Programming (Week 5-6)**
• Classes and objects
• Inheritance and methods
• Special methods (__init__, __str__)

**Next Steps:** Web frameworks (Django/Flask), Data Science (pandas/numpy), or AI/ML

"""
    
    def _get_javascript_tutorial(self) -> str:
        """JavaScript-specific tutorial content"""
        return """**JavaScript Learning Path:**

**1. JavaScript Fundamentals (Week 1-2)**
• Variables (var, let, const)
• Data types and operators
• Functions and arrow functions

**2. DOM Manipulation (Week 2-3)**
• Selecting elements
• Event handling
• Modifying HTML/CSS dynamically

**3. Asynchronous JavaScript (Week 3-4)**
• Callbacks and promises
• async/await
• Fetch API for HTTP requests

**4. Modern JavaScript (Week 4-5)**
• ES6+ features
• Modules and imports
• Destructuring and spread operator

**5. Frameworks & Libraries (Week 5+)**
• React, Vue, or Angular basics
• Node.js for backend development

**Next Steps:** Full-stack development, React/Vue mastery, or Node.js backend

"""
    
    def _get_java_tutorial(self) -> str:
        """Java-specific tutorial content"""
        return """**Java Learning Path:**

**1. Java Basics (Week 1-2)**
• Classes and objects
• Variables and data types
• Methods and constructors

**2. Object-Oriented Programming (Week 2-4)**
• Inheritance and polymorphism
• Encapsulation and abstraction
• Interfaces and abstract classes

**3. Collections and Generics (Week 4-5)**
• ArrayList, HashMap, LinkedList
• Iterators and enhanced for loops
• Generic types and wildcards

**4. Exception Handling (Week 5-6)**
• Try-catch blocks
• Custom exceptions
• Finally and resource management

**5. Advanced Topics (Week 6+)**
• Multithreading and concurrency
• File I/O and networking
• Spring framework basics

**Next Steps:** Spring Boot, Android development, or enterprise Java

"""
    
    def _get_cpp_tutorial(self) -> str:
        """C++-specific tutorial content"""
        return """**C++ Learning Path:**

**1. C++ Fundamentals (Week 1-3)**
• Variables, data types, operators
• Control structures and loops
• Functions and function overloading

**2. Object-Oriented Programming (Week 3-5)**
• Classes and objects
• Constructors and destructors
• Inheritance and virtual functions

**3. Memory Management (Week 5-6)**
• Pointers and references
• Dynamic memory allocation
• Smart pointers (unique_ptr, shared_ptr)

**4. STL (Standard Template Library) (Week 6-7)**
• Containers (vector, map, set)
• Iterators and algorithms
• Function templates and lambdas

**5. Advanced Topics (Week 7+)**
• Templates and generic programming
• Exception handling
• Multi-threading with std::thread

**Next Steps:** Game development, system programming, or embedded systems

"""
    
    def _get_react_tutorial(self) -> str:
        """React-specific tutorial content"""
        return """**React Learning Path:**

**1. React Basics (Week 1-2)**
• Components and JSX
• Props and state
• Event handling

**2. Component Lifecycle (Week 2-3)**
• useEffect hook
• useState and other hooks
• Conditional rendering

**3. State Management (Week 3-4)**
• Context API
• Redux basics
• Component communication

**4. Routing and Navigation (Week 4-5)**
• React Router
• Dynamic routing
• Protected routes

**5. Advanced React (Week 5+)**
• Custom hooks
• Performance optimization
• Testing with Jest and React Testing Library

**Next Steps:** Next.js, TypeScript with React, or full-stack development

"""
    
    def _get_beginner_tutorial(self) -> str:
        """Beginner programming tutorial"""
        return """**Programming Fundamentals for Beginners:**

**Understanding Programming:**
Programming is like giving instructions to a computer in a language it understands.

**Core Concepts:**

**1. Variables** - Storage containers for data
• Think of variables like labeled boxes that hold information
• Examples: name = "John", age = 25, is_student = True

**2. Data Types** - Different kinds of information
• Numbers: integers (5) and decimals (3.14)
• Text: strings ("Hello World")
• True/False: booleans (True, False)
• Collections: lists [1, 2, 3] and dictionaries {"name": "John"}

**3. Control Structures** - Decision making and repetition
• if/else: Make decisions based on conditions
• loops: Repeat actions multiple times
• functions: Group instructions together for reuse

**4. Problem Solving Steps:**
1. Understand the problem clearly
2. Break it down into smaller steps
3. Write code step by step
4. Test and debug your solution
5. Improve and optimize

**Getting Started Tips:**
• Start with simple programs and gradually increase complexity
• Practice daily, even if just for 15 minutes
• Don't be afraid to make mistakes - they're learning opportunities!
• Read error messages carefully - they often tell you exactly what's wrong
• Comment your code to remember what each part does

**"""
    
    def _get_data_structures_tutorial(self) -> str:
        """Data structures tutorial content"""
        return """**Data Structures Learning Path:**

**1. Arrays and Lists**
• Ordered collections of elements
• Accessing elements by index
• Common operations: add, remove, search

**2. Stacks and Queues**
• Stack: Last In, First Out (LIFO) - like a stack of plates
• Queue: First In, First Out (FIFO) - like a line at a store
• Perfect for managing order of operations

**3. Linked Lists**
• Elements connected through pointers/references
• Dynamic size, efficient insertion/deletion
• Trade-off: no random access like arrays

**4. Trees and Graphs**
• Tree: Hierarchical structure with root and branches
• Graph: Nodes connected by edges, can have cycles
• Used in file systems, social networks, algorithms

**5. Hash Tables/Dictionaries**
• Key-value pairs for fast lookup
• Constant time access on average
• Perfect for caching and counting

**Practical Applications:**
• Lists: Shopping carts, user management
• Stacks: Undo operations, function calls
• Queues: Task scheduling, breadth-first search
• Trees: File systems, decision trees
• Hash tables: Database indexing, caching

"""

    def _get_algorithms_tutorial(self) -> str:
        """Algorithms tutorial content"""
        return """**Algorithms Learning Path:**

**1. Sorting Algorithms**
• Bubble Sort: Simple but inefficient comparison-based sorting
• Quick Sort: Divide-and-conquer approach, very efficient
• Merge Sort: Stable, guaranteed O(n log n) performance
• Selection Sort: Find minimum and swap

**2. Searching Algorithms**
• Linear Search: Check each element one by one
• Binary Search: Efficient search in sorted arrays
• Hash-based Search: Instant lookup using hash tables

**3. Recursion**
• Function calling itself with smaller problem
• Base case prevents infinite recursion
• Examples: Factorial, Fibonacci, tree traversal

**4. Dynamic Programming**
• Break complex problems into simpler subproblems
• Store results to avoid recalculation
• Examples: Coin change, longest subsequence

**5. Graph Algorithms**
• Breadth-First Search (BFS): Level-by-level exploration
• Depth-First Search (DFS): Go as deep as possible first
• Dijkstra's Algorithm: Shortest path finding

**Time Complexity Basics:**
• O(1): Constant time - hash table lookup
• O(log n): Logarithmic - binary search
• O(n): Linear - simple loop
• O(n²): Quadratic - nested loops

"""

    def _get_web_development_tutorial(self) -> str:
        """Web development tutorial content"""
        return """**Web Development Learning Path:**

**1. HTML Foundation**
• Structure: headers, paragraphs, lists, links
• Forms: input fields, buttons, validation
• Semantic elements: nav, main, section, article

**2. CSS Styling**
• Selectors: target specific elements
• Box model: margin, border, padding, content
• Layout: flexbox and grid for responsive design
• Animations and transitions

**3. JavaScript Fundamentals**
• DOM manipulation: change webpage content dynamically
• Event handling: respond to user interactions
• Asynchronous programming: fetch data from servers

**4. Responsive Design**
• Mobile-first approach
• Media queries for different screen sizes
• Flexible layouts and images

**5. Frontend Frameworks**
• React: Component-based UI development
• Vue.js: Progressive framework for building UIs
• Angular: Full-featured framework for large apps

**Project Ideas:**
• Personal portfolio website
• Todo list application
• Weather dashboard
• Blog or news site
• E-commerce product page

"""

    def _get_debugging_tutorial(self) -> str:
        """Debugging tutorial content"""
        return """**Debugging Techniques Tutorial:**

**1. Reading Error Messages**
• Error type tells you what went wrong
• Line number shows where the error occurred
• Stack trace shows the path to the error

**2. Using Debuggers**
• Set breakpoints to pause execution
• Step through code line by line
• Inspect variable values at runtime

**3. Print/Log Debugging**
• Add print statements to track code flow
• Log variable values at key points
• Use different log levels (info, warning, error)

**4. Common Bug Patterns**
• Off-by-one errors in loops and arrays
• Null/undefined reference errors
• Type mismatches and conversion issues
• Scope and variable naming conflicts

**5. Testing Strategies**
• Unit tests: Test individual functions
• Integration tests: Test component interactions
• Edge case testing: Test boundary conditions
• Regression testing: Ensure fixes don't break existing code

**Debugging Mindset:**
• Stay calm and systematic
• Reproduce the bug consistently
• Isolate the problem area
• Test one change at a time
• Keep detailed notes of what you tried

**Tools and Techniques:**
• IDE debuggers and breakpoints
• Browser developer tools for web development
• Logging frameworks and error tracking
• Automated testing suites

"""