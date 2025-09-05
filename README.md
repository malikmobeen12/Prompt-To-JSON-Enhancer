# Prompt-to-JSON Enhancer

A modern web application that transforms plain text prompts into structured JSON using intelligent rule-based logic.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd prompt-to-json-enhancer
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the application
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

## ✨ Features

- **Intelligent Analysis**: Detects context (generate code, debug, explain) and programming languages
- **Modern UI**: Floating action button, dark/light mode, responsive design
- **API Endpoints**: RESTful API with caching and customization options
- **Production Ready**: Dockerized with AWS deployment support

## 📁 Project Structure

```
prompt-to-json-enhancer/
├── app.py                 # Main Flask application
├── utils/                 # Modular components
│   ├── context_detector.py    # Context classification
│   ├── language_detector.py   # Language detection
│   ├── solution_builder.py    # Solution generation
│   └── prompt_analyzer.py     # Main orchestration
├── templates/
│   └── index.html         # Main UI template
├── static/
│   ├── css/style.css      # Modern styling
│   └── js/app.js          # Frontend logic
├── Dockerfile             # Container configuration
└── requirements.txt       # Python dependencies
```

## 🔌 API Usage

### Transform Prompt
```bash
curl -X POST http://localhost:5000/transform \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python function to calculate factorial"}'
```

### Custom Transform
```bash
curl -X POST http://localhost:5000/transform/custom \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python function", "include_keys": ["context", "output_format"], "output_style": "short"}'
```

## 🐳 Docker

```bash
# Build and run
docker build -t prompt-to-json-enhancer .
docker run -p 5000:5000 prompt-to-json-enhancer
```

## 📝 Example

**Input:**
```
Write a Python function to scrape a website and save results to CSV
```

**Output:**
```json
{
  "context": "The user is asking an AI assistant to generate code or create a technical solution.",
  "problem": "Write a Python function to scrape a website and save results to CSV",
  "expected_solution": "A complete, working code solution that addresses the requirements. The solution should include Python code with proper imports and structure, web scraping or HTTP requests, CSV file generation and data export.",
  "output_format": "Code in Python"
}
```

## 🛠️ Technology Stack

- **Backend**: Flask 2.3.3, Gunicorn
- **Frontend**: HTML5/CSS3/JavaScript, Prism.js
- **Container**: Docker
- **Cloud**: AWS ECS (optional)
