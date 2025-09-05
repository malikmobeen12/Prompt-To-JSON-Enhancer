"""
Main prompt analyzer that orchestrates the transformation process
"""

from .context_detector import detect_context
from .language_detector import detect_language
from .solution_builder import build_expected_solution


def transform_prompt_to_json(prompt):
    """
    Transform a plain text prompt into structured JSON using enhanced rule-based logic.
    
    Args:
        prompt (str): The input prompt text
        
    Returns:
        dict: Structured JSON with context, problem, expected_solution, output_format
    """
    prompt_lower = prompt.lower()
    
    # Detect context
    context = detect_context(prompt_lower)
    
    # Detect language and technology
    output_format, tech_details = detect_language(prompt_lower)
    
    # Build expected solution
    expected_solution = build_expected_solution(context, tech_details, prompt_lower)
    
    return {
        "context": context,
        "problem": prompt.strip(),
        "expected_solution": expected_solution,
        "output_format": output_format
    }
