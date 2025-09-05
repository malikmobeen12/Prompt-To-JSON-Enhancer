"""
Language and technology detection for prompts
"""


def detect_language(prompt_lower):
    """
    Detect the programming language or technology from the prompt.
    
    Args:
        prompt_lower (str): Lowercase version of the prompt
        
    Returns:
        tuple: (output_format: str, tech_details: dict)
    """
    # Define language detection patterns with priority order (Python > JS > SQL > Text)
    language_patterns = {
        "Python": {
            "keywords": ["import ", "def ", "class ", "script", ".py", "pandas", "numpy", "requests", "flask", "django", "csv"],
            "context_words": ["python", "py", "pip", "conda", "virtualenv"],
            "exclude_words": ["sql", "javascript", "java", "html", "css", "explain", "describe", "what is", "how does"]
        },
        "JavaScript": {
            "keywords": ["function", "const ", "let ", "=>", "document", "window", "async", "await", "promise"],
            "context_words": ["javascript", "js", "node", "npm", "yarn"],
            "exclude_words": ["python", "sql", "java", "html", "css", "explain", "describe", "what is", "how does"]
        },
        "SQL": {
            "keywords": ["select", "from", "where", "join", "insert", "update", "delete", "create table", "alter table", "drop table", "group by", "having", "order by"],
            "context_words": ["sql", "query", "database", "table", "column"],
            "exclude_words": ["python", "javascript", "java", "html", "css", "explain", "describe", "what is", "how does"]
        },
        "Bash": {
            "keywords": ["#!/bin/bash", "#!/bin/sh", "echo", "grep", "awk", "sed", "chmod", "sudo", "cron", "systemctl"],
            "context_words": ["bash", "shell", "terminal", "command line"],
            "exclude_words": ["python", "javascript", "sql", "java", "r script", "r language", "explain", "describe", "what is", "how does"]
        },
        "R": {
            "keywords": ["library(", "data.frame", "ggplot", "dplyr", "tidyverse", "read.csv", "lm(", "summary("],
            "context_words": [" r ", "rscript", "rstudio", "r language", "r script"],
            "exclude_words": ["python", "javascript", "sql", "java", "bash", "react", "vue", "explain", "describe", "what is", "how does"]
        },
        "Ruby": {
            "keywords": ["def ", "class ", "require", "gem", "rails", "sinatra", "puts", "gets"],
            "context_words": ["ruby", "rb", "rails", "gem"],
            "exclude_words": ["python", "javascript", "sql", "java", "explain", "describe", "what is", "how does"]
        },
        "HTML/CSS": {
            "keywords": ["<html", "<div", "<p", "<h1", "css", "style", "class=", "id=", "margin", "padding", "color"],
            "context_words": ["html", "css", "webpage", "website", "frontend"],
            "exclude_words": ["python", "javascript", "sql", "java", "explain", "describe", "what is", "how does"]
        },
        "Java": {
            "keywords": ["public class", "private", "public static", "main(", "import java", "spring", "maven", "gradle"],
            "context_words": ["java", "jvm", "spring", "maven", "gradle"],
            "exclude_words": ["python", "javascript", "sql", "html", "css", "explain", "describe", "what is", "how does"]
        }
    }
    
    # Detect language with priority system
    detected_language = None
    confidence_scores = {}
    
    for language, pattern in language_patterns.items():
        score = 0
        
        # Check for context words
        for word in pattern["context_words"]:
            if word in prompt_lower:
                score += 2
        
        # Check for keywords
        for keyword in pattern["keywords"]:
            if keyword in prompt_lower:
                score += 1
        
        # Reduce score if exclude words are present
        for exclude_word in pattern["exclude_words"]:
            if exclude_word in prompt_lower:
                score -= 1
        
        if score > 0:
            confidence_scores[language] = score
    
    # Initialize default values
    output_format = "Text response"
    tech_details = {}
    
    # Check for special cases first (frameworks/components) - but avoid false triggers in explanations
    special_case_detected = False
    
    # Only apply special cases if not in explanation context
    is_explanation_context = any(word in prompt_lower for word in ["explain", "describe", "what is", "how does", "difference", "meaning", "concept"])
    
    if not is_explanation_context:
        if "react" in prompt_lower:
            output_format = "React component"
            tech_details["framework"] = "React"
            special_case_detected = True
        elif "vue" in prompt_lower:
            output_format = "Vue component"
            tech_details["framework"] = "Vue"
            special_case_detected = True
        elif "docker" in prompt_lower:
            output_format = "Docker configuration"
            tech_details["containerization"] = True
            if "compose" in prompt_lower:
                tech_details["docker_compose"] = True
            special_case_detected = True
        elif any(word in prompt_lower for word in ["api", "endpoint", "rest", "graphql"]) and any(word in prompt_lower for word in ["write", "create", "build", "make", "generate", "develop", "implement"]) and not any(word in prompt_lower for word in ["python", "javascript", "java", "sql"]):
            output_format = "API specification"
            tech_details["api"] = True
            if "rest" in prompt_lower:
                tech_details["api_type"] = "REST"
            elif "graphql" in prompt_lower:
                tech_details["api_type"] = "GraphQL"
            special_case_detected = True
    
    # Use language detection if no special cases matched
    if not special_case_detected and confidence_scores:
        detected_language = max(confidence_scores, key=confidence_scores.get)
        
        # Set output format and tech details based on detected language
        if detected_language == "Python":
            output_format = "Code in Python"
            tech_details["language"] = "Python"
            if "csv" in prompt_lower:
                tech_details["output"] = "CSV file"
            if any(word in prompt_lower for word in ["database", "db", "postgresql", "mysql", "sqlite"]):
                tech_details["database"] = True
            if any(word in prompt_lower for word in ["web", "scrape", "requests", "urllib"]):
                tech_details["web"] = True
            if any(word in prompt_lower for word in ["error", "exception", "try", "except"]):
                tech_details["error_handling"] = True
                
        elif detected_language == "SQL":
            output_format = "SQL query"
            tech_details["language"] = "SQL"
            if any(keyword in prompt_lower for keyword in ["join", "inner join", "left join", "right join", "outer join"]):
                tech_details["joins"] = True
            if any(keyword in prompt_lower for keyword in ["sum", "count", "avg", "max", "min", "group by", "having"]):
                tech_details["aggregation"] = True
            if any(keyword in prompt_lower for keyword in ["insert", "update", "delete"]):
                tech_details["data_modification"] = True
                
        elif detected_language == "JavaScript":
            output_format = "Code in JavaScript"
            tech_details["language"] = "JavaScript"
            if "react" in prompt_lower:
                tech_details["framework"] = "React"
            elif "vue" in prompt_lower:
                tech_details["framework"] = "Vue"
            elif "node" in prompt_lower:
                tech_details["runtime"] = "Node.js"
                
        elif detected_language == "Bash":
            output_format = "Bash script"
            tech_details["language"] = "Bash"
            if any(word in prompt_lower for word in ["automation", "cron", "schedule"]):
                tech_details["automation"] = True
                
        elif detected_language == "R":
            output_format = "R script"
            tech_details["language"] = "R"
            if any(word in prompt_lower for word in ["data", "analysis", "statistics", "visualization"]):
                tech_details["data_analysis"] = True
                
        elif detected_language == "Ruby":
            output_format = "Code in Ruby"
            tech_details["language"] = "Ruby"
            if "rails" in prompt_lower:
                tech_details["framework"] = "Rails"
            elif "sinatra" in prompt_lower:
                tech_details["framework"] = "Sinatra"
                
        elif detected_language == "HTML/CSS":
            output_format = "HTML/CSS code"
            tech_details["web"] = True
            if "responsive" in prompt_lower:
                tech_details["responsive"] = True
                
        elif detected_language == "Java":
            output_format = "Code in Java"
            tech_details["language"] = "Java"
            if "spring" in prompt_lower:
                tech_details["framework"] = "Spring"
    
    return output_format, tech_details
