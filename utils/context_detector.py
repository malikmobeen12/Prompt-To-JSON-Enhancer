"""
Context detection for prompt classification
"""


def detect_context(prompt_lower):
    """
    Detect the primary context/intent of the prompt.
    
    Args:
        prompt_lower (str): Lowercase version of the prompt
        
    Returns:
        str: The detected context
    """
    # Enhanced context detection with better intent classification
    context_keywords = {
        "explain": ["explain", "what is", "how does", "describe", "tell me about", "understand", "meaning", "definition", "concept", "why", "when", "where", "difference", "between"],
        "professional_writing": ["professional email", "business email", "business letter", "formal letter", "meeting request", "business proposal", "report", "memo", "presentation", "cover letter", "resume", "cv"],
        "generate_code": ["write", "create", "build", "make", "generate", "develop", "implement", "code", "script", "function", "program", "class", "method"],
        "debug_fix": ["debug", "fix", "error", "issue", "problem", "bug", "troubleshoot", "resolve", "correct", "repair", "broken", "not working", "failing", "exception", "crash", "hang"],
        "optimize": ["optimize", "improve", "enhance", "performance", "faster", "better", "efficient", "refactor", "speed up", "optimize"],
        "analyze": ["analyze", "review", "evaluate", "assess", "examine", "inspect", "check", "validate", "compare", "contrast"],
        "design": ["design", "architecture", "structure", "plan", "strategy", "approach", "methodology", "blueprint", "framework"]
    }
    
    # Detect primary context
    context_scores = {}
    for context_type, keywords in context_keywords.items():
        score = sum(1 for keyword in keywords if keyword in prompt_lower)
        if score > 0:
            context_scores[context_type] = score
    
    # Determine primary context
    if context_scores:
        primary_context = max(context_scores, key=context_scores.get)
        if primary_context == "generate_code":
            return "The user is asking an AI assistant to generate code or create a technical solution."
        elif primary_context == "debug_fix":
            return "The user is asking an AI assistant to debug, fix, or troubleshoot an issue."
        elif primary_context == "explain":
            return "The user is asking an AI assistant to explain a concept or provide educational information."
        elif primary_context == "professional_writing":
            return "The user is asking an AI assistant to provide information or assistance."
        elif primary_context == "optimize":
            return "The user is asking an AI assistant to optimize or improve existing code or processes."
        elif primary_context == "analyze":
            return "The user is asking an AI assistant to analyze, review, or evaluate something."
        elif primary_context == "design":
            return "The user is asking an AI assistant to design or architect a solution."
    
    # Default context
    return "The user is asking an AI assistant to provide information or assistance."
