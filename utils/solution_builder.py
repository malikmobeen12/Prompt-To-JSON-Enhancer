"""
Expected solution builder for different prompt types
"""


def build_expected_solution(context, tech_details, prompt_lower):
    """
    Build a detailed expected solution based on context and technology details.
    
    Args:
        context (str): The detected context
        tech_details (dict): Technology-specific details
        prompt_lower (str): Lowercase version of the prompt
        
    Returns:
        str: The expected solution description
    """
    base_solutions = {
        "generate_code": "A complete, working code solution that addresses the requirements.",
        "debug_fix": "A solution that identifies and fixes the issue with clear explanations.",
        "explain": "A clear, comprehensive explanation with examples and context.",
        "professional_writing": "A professional and well-structured document with appropriate formatting and language.",
        "optimize": "An optimized solution with performance improvements and best practices.",
        "analyze": "A detailed analysis with findings, recommendations, and insights.",
        "design": "A well-structured design with clear architecture and implementation guidance."
    }
    
    # Get base solution
    if "generate code" in context.lower():
        base = base_solutions["generate_code"]
    elif "debug" in context.lower() or "fix" in context.lower():
        base = base_solutions["debug_fix"]
    elif "explain" in context.lower():
        base = base_solutions["explain"]
    elif "provide information or assistance" in context.lower() and any(word in prompt_lower for word in ["professional email", "business email", "business letter", "formal letter", "meeting request", "business proposal", "report", "memo", "presentation", "cover letter", "resume", "cv"]):
        base = base_solutions["professional_writing"]
    elif "optimize" in context.lower():
        base = base_solutions["optimize"]
    elif "analyze" in context.lower():
        base = base_solutions["analyze"]
    elif "design" in context.lower():
        base = base_solutions["design"]
    else:
        base = base_solutions["generate_code"]
    
    # Detect multi-step tasks - only flag if multiple distinct operations exist
    multi_step_indicators = ["and", "then", "also", "next", "after", "finally", "followed by"]
    sequence_indicators = ["first", "second", "third", "step 1", "step 2", "step 3"]
    
    # Check for sequence indicators
    has_sequence = any(indicator in prompt_lower for indicator in sequence_indicators)
    
    # Check for multi-step indicators with careful validation
    has_multi_step = False
    if any(indicator in prompt_lower for indicator in multi_step_indicators):
        # Only consider it multi-step if there are multiple distinct operations
        operation_indicators = [
            "read", "write", "create", "delete", "update", "insert", "fetch", "download", "upload",
            "connect", "disconnect", "import", "export", "parse", "validate", "transform", "filter",
            "sort", "group", "join", "merge", "split", "extract", "generate", "process", "analyze",
            "scrape", "save", "load", "store", "retrieve", "calculate", "compute", "format"
        ]
        
        # Count distinct operations
        operation_count = sum(1 for op in operation_indicators if op in prompt_lower)
        
        # Only mark as multi-step if:
        # 1. Has explicit sequence indicators, OR
        # 2. Has 2+ distinct operations with multi-step indicators
        has_multi_step = has_sequence or (operation_count >= 2 and any(indicator in prompt_lower for indicator in multi_step_indicators))
    
    # Add specific details based on technology
    details = []
    
    if tech_details.get("language") == "Python":
        details.append("Python code with proper imports and structure")
        if tech_details.get("database"):
            details.append("database connection and query handling")
        if tech_details.get("web"):
            details.append("web scraping or HTTP requests")
        if tech_details.get("output") == "CSV file":
            details.append("CSV file generation and data export")
        if tech_details.get("error_handling"):
            details.append("comprehensive error handling and exception management")
            
    elif tech_details.get("framework") == "React":
        details.append("React component with hooks and proper state management")
            
    elif tech_details.get("language") == "SQL":
        details.append("SQL query with proper syntax and optimization")
        if tech_details.get("joins"):
            details.append("appropriate table joins")
        if tech_details.get("aggregation"):
            details.append("aggregation functions and grouping")
        if tech_details.get("data_modification"):
            details.append("data modification operations (INSERT/UPDATE/DELETE)")
            
    elif tech_details.get("language") == "JavaScript":
        details.append("JavaScript code with modern ES6+ features")
        if tech_details.get("framework") == "React":
            details.append("React component with hooks and proper state management")
        elif tech_details.get("framework") == "Vue":
            details.append("Vue component with composition API")
        elif tech_details.get("runtime") == "Node.js":
            details.append("Node.js server-side implementation")
            
    elif tech_details.get("language") == "Bash":
        details.append("Bash script with proper shebang and error handling")
        if tech_details.get("automation"):
            details.append("automation and scheduling capabilities")
            
    elif tech_details.get("language") == "R":
        details.append("R script with proper library imports")
        if tech_details.get("data_analysis"):
            details.append("data analysis and visualization")
            
    elif tech_details.get("language") == "Ruby":
        details.append("Ruby code with proper structure and conventions")
        if tech_details.get("framework") == "Rails":
            details.append("Rails framework implementation")
        elif tech_details.get("framework") == "Sinatra":
            details.append("Sinatra web framework")
            
    elif tech_details.get("web") and "html" in prompt_lower:
        details.append("HTML structure with CSS styling")
        if tech_details.get("responsive"):
            details.append("responsive design implementation")
            
    elif tech_details.get("framework") == "React":
        details.append("React component with hooks and proper state management")
    
    # Add professional writing specific details
    if "provide information or assistance" in context.lower() and any(word in prompt_lower for word in ["professional email", "business email", "business letter", "formal letter", "meeting request", "business proposal", "report", "memo", "presentation", "cover letter", "resume", "cv"]):
        if "email" in prompt_lower:
            details.append("proper email formatting with subject line and professional tone")
        if "meeting" in prompt_lower:
            details.append("clear meeting request with proposed time and agenda")
        if "business" in prompt_lower:
            details.append("business-appropriate language and structure")
        if "professional" in prompt_lower:
            details.append("professional tone and formatting")
    
    # Add context-specific enhancements
    if "error" in prompt_lower or "exception" in prompt_lower:
        details.append("error handling and validation")
    if "test" in prompt_lower:
        details.append("unit tests and test cases")
    if "documentation" in prompt_lower or "comment" in prompt_lower:
        details.append("comprehensive documentation and comments")
    if "security" in prompt_lower:
        details.append("security best practices and considerations")
    if "performance" in prompt_lower:
        details.append("performance optimization techniques")
    
    # Handle multi-step tasks - only add multi-step description if truly multi-step
    if has_multi_step:
        base = base.replace("solution", "multi-step solution with clear sequence of operations")
        # Only add sequencing detail if it's a complex multi-step process
        if has_sequence or len(details) > 3:
            details.append("step-by-step implementation with proper sequencing")
    
    # Combine base solution with specific details, avoiding redundancy
    if details:
        # Remove redundant phrases
        filtered_details = []
        for detail in details:
            # Avoid adding redundant error handling if already mentioned
            if "error handling" in detail and any("error" in d for d in filtered_details):
                continue
            # Avoid adding redundant database details if already mentioned
            if "database" in detail and any("database" in d for d in filtered_details):
                continue
            # Avoid adding redundant web details if already mentioned
            if "web" in detail and any("web" in d for d in filtered_details):
                continue
            filtered_details.append(detail)
        
        if filtered_details:
            return f"{base} The solution should include {', '.join(filtered_details)}."
        else:
            return base
    else:
        return base
