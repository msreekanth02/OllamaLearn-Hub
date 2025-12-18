"""
Flask Web Interface for Ollama Learning Project
==============================================
Simple web-based frontend for Ollama examples.

Install: pip install flask
Run: python3 app.py
Visit: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODELS_API = "http://localhost:11434/api/tags"
DEFAULT_MODEL = "neural-chat"


def get_available_models():
    """Get list of available models from Ollama."""
    try:
        response = requests.get(MODELS_API)
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except Exception as e:
        return [DEFAULT_MODEL]


def query_ollama(prompt, model=DEFAULT_MODEL, temperature=0.7, stream=False):
    """Query Ollama with given prompt and parameters."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
        "temperature": temperature,
    }
    
    try:
        response = requests.post(OLLAMA_API, json=payload, timeout=60)
        response.raise_for_status()
        
        if stream:
            return response
        else:
            result = response.json()
            return {
                "response": result.get("response", ""),
                "tokens": result.get("eval_count", 0),
                "duration": result.get("total_duration", 0) / 1e9,
                "status": "success"
            }
    except requests.exceptions.ConnectionError:
        return {
            "response": "❌ Error: Cannot connect to Ollama API. Make sure to run 'ollama serve'",
            "status": "error"
        }
    except requests.exceptions.Timeout:
        return {
            "response": "❌ Error: Request timed out. Try a simpler prompt.",
            "status": "error"
        }
    except Exception as e:
        return {
            "response": f"❌ Error: {str(e)}",
            "status": "error"
        }


@app.route("/")
def index():
    """Home page - Basic Request example."""
    models = get_available_models()
    return render_template("index.html", models=models)


@app.route("/streaming")
def streaming():
    """Streaming responses page."""
    models = get_available_models()
    return render_template("streaming.html", models=models)


@app.route("/chat")
def chat():
    """Multi-turn conversation page."""
    models = get_available_models()
    return render_template("chat.html", models=models)


@app.route("/prompting")
def prompting():
    """Prompt engineering examples page."""
    models = get_available_models()
    return render_template("prompting.html", models=models)


@app.route("/advanced")
def advanced():
    """Advanced features page."""
    models = get_available_models()
    return render_template("advanced.html", models=models)


# API Endpoints

@app.route("/api/generate", methods=["POST"])
def api_generate():
    """API endpoint for simple text generation."""
    data = request.json
    prompt = data.get("prompt", "")
    model = data.get("model", DEFAULT_MODEL)
    temperature = float(data.get("temperature", 0.7))
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    result = query_ollama(prompt, model, temperature, stream=False)
    response = jsonify(result)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


@app.route("/api/models", methods=["GET"])
def api_models():
    """Get list of available models."""
    try:
        response = requests.get(MODELS_API)
        models = response.json().get("models", [])
        return jsonify({
            "models": [{
                "name": m["name"],
                "size": m.get("size", 0) / (1024**3)  # Convert to GB
            } for m in models],
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


@app.route("/api/status", methods=["GET"])
def api_status():
    """Check Ollama server status."""
    try:
        response = requests.get(MODELS_API)
        response.raise_for_status()
        return jsonify({
            "status": "online",
            "server": "Ollama is running",
            "version": "1.0"
        })
    except Exception as e:
        return jsonify({
            "status": "offline",
            "error": "Cannot connect to Ollama server",
            "help": "Run 'ollama serve' in another terminal"
        }), 503


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 Ollama Web Interface")
    print("="*60)
    print("\n📱 Opening http://localhost:5001")
    print("📚 Available pages:")
    print("   • Basic Requests: /")
    print("   • Streaming: /streaming")
    print("   • Chat: /chat")
    print("   • Prompting: /prompting")
    print("   • Advanced: /advanced")
    print("\n⚠️  Make sure Ollama server is running: ollama serve")
    print("="*60 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5001)
