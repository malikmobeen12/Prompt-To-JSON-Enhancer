"""
Prompt-to-JSON Enhancer Web App
Flask backend with modular prompt transformation logic
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils import validate_prompt, get_cache_key, transform_prompt_to_json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Simple in-memory cache for transformations
transformation_cache = {}


@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')


@app.route('/transform', methods=['POST'])
def transform():
    """
    Transform endpoint that accepts a prompt and returns structured JSON
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing 'prompt' field in request body"
            }), 400
        
        prompt = data['prompt']
        
        # Validate the prompt
        is_valid, error_message = validate_prompt(prompt)
        if not is_valid:
            return jsonify({
                "error": error_message
            }), 400
        
        # Check cache first
        cache_key = get_cache_key(prompt)
        if cache_key in transformation_cache:
            result = transformation_cache[cache_key]
            result["cached"] = True
            return jsonify(result)
        
        # Transform the prompt to JSON
        result = transform_prompt_to_json(prompt)
        result["cached"] = False
        
        # Cache the result (limit cache size to prevent memory issues)
        if len(transformation_cache) < 1000:
            transformation_cache[cache_key] = result
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/transform/custom', methods=['POST'])
def transform_custom():
    """
    Transform endpoint with customization options
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing 'prompt' field in request body"
            }), 400
        
        prompt = data['prompt']
        include_keys = data.get('include_keys', ['context', 'problem', 'expected_solution', 'output_format'])
        output_style = data.get('output_style', 'detailed')  # 'short' or 'detailed'
        
        # Validate the prompt
        is_valid, error_message = validate_prompt(prompt)
        if not is_valid:
            return jsonify({
                "error": error_message
            }), 400
        
        # Transform the prompt to JSON
        result = transform_prompt_to_json(prompt)
        
        # Apply customization
        if output_style == 'short':
            if 'expected_solution' in result:
                result['expected_solution'] = result['expected_solution'].split('.')[0] + '.'
        
        # Filter keys based on user selection
        filtered_result = {key: result[key] for key in include_keys if key in result}
        filtered_result["cached"] = False
        
        return jsonify(filtered_result)
        
    except Exception as e:
        return jsonify({
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the transformation cache"""
    global transformation_cache
    transformation_cache.clear()
    return jsonify({"message": "Cache cleared successfully"})


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "prompt-to-json-enhancer"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
