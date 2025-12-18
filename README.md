# Ollama Learning Project - Complete Guide

A beginner-friendly learning platform for understanding Ollama and large language models through Python scripts and an interactive web interface.

## What is Ollama?

Ollama is an open-source framework that makes it easy to run and manage large language models (LLMs) locally on your machine. Instead of relying on cloud services, you can run AI models directly on your computer with simple commands and APIs.

## System Requirements

Before getting started, ensure you have:

1. **Ollama installed**: Download from https://ollama.ai
2. **Python 3.8 or higher**: Check with `python3 --version`
3. **Git**: For cloning/managing the project
4. **At least 4GB RAM**: Minimum for running models (8GB+ recommended)
5. **Disk space**: 5-10GB for downloading models

## Installation Steps

### Step 1: Install Ollama

1. Visit https://ollama.ai
2. Download the installer for your operating system
3. Follow the installation wizard
4. Verify installation by running:
   ```bash
   ollama --version
   ```

### Step 2: Set Up Python Environment

1. Clone or download this project
2. Navigate to the project folder:
   ```bash
   cd ollamatest
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
4. Activate the virtual environment:

   On macOS/Linux:
   ```bash
   source .venv/bin/activate
   ```
   
   On Windows:
   ```bash
   .venv\Scripts\activate
   ```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- requests: For making HTTP calls to Ollama API
- ollama: Python SDK for Ollama
- flask: Web framework for the interface

### Step 4: Download Models

Open a terminal and run:
```bash
ollama pull neural-chat
ollama pull mistral
```

You now have everything needed to get started!

## Quick Start

### Running the Web Interface (Recommended for Beginners)

This is the easiest way to learn Ollama. It provides a visual interface with interactive examples.

1. Open Terminal 1 and start the Ollama server:
   ```bash
   ollama serve
   ```

2. Open Terminal 2, activate the environment, and start the Flask app:
   ```bash
   source .venv/bin/activate
   python3 app.py
   ```

3. Open your web browser and visit:
   ```
   http://localhost:5001
   ```

You should see the learning interface with 5 modules to explore.

### Running Python Scripts

If you prefer command-line examples:

1. Start Ollama in one terminal:
   ```bash
   ollama serve
   ```

2. In another terminal, run any example:
   ```bash
   source .venv/bin/activate
   python3 src/1_basic_request.py
   ```

## Project Structure

### Python Learning Examples

These scripts teach you step-by-step how to use Ollama. Located in the `src/` directory:

- **src/1_basic_request.py**: Simple API request to get responses
- **src/2_streaming_response.py**: Get responses in real-time chunks
- **src/3_conversation.py**: Build multi-turn conversations with memory
- **src/4_prompt_engineering.py**: Compare vague vs specific prompts
- **src/5_python_client.py**: Use the Ollama Python SDK
- **src/6_advanced_usage.py**: Advanced parameters and configuration

### Web Interface Files

- **app.py**: Main Flask application server
- **templates/**: HTML pages for the web interface
  - index.html: Basic requests module
  - streaming.html: Real-time responses
  - chat.html: Conversation interface
  - prompting.html: Prompt engineering lessons
  - advanced.html: Advanced features
- **static/style.css**: Styling for web interface

### Configuration Files

- **requirements.txt**: Python package dependencies

## Learning Path for Beginners

### Level 1: Understanding Basics (15 minutes)
1. Start the web interface
2. Visit the "Basic Requests" page
3. Try asking simple questions
4. Observe how temperature affects responses

### Level 2: Exploring Features (30 minutes)
1. Try the "Streaming" page to see real-time responses
2. Use the "Chat" page to have conversations
3. Observe how context helps the AI understand

### Level 3: Advanced Concepts (45 minutes)
1. Visit "Prompt Engineering" to compare prompt quality
2. Try "Advanced" page to test temperature settings
3. Compare different models' responses

### Level 4: Python Scripts (1 hour)
1. Run `src/1_basic_request.py` to see what happens
2. Modify the prompt and run again
3. Try other scripts in the src/ folder to understand API calls

## Key Concepts Explained

### Model
An AI model is a trained neural network that understands text. Different models have different strengths:
- neural-chat: Good for conversations, fast
- mistral: Fast and general-purpose
- llama3.2: Larger, more capable

### Prompt
A prompt is your question or instruction to the AI. The quality of your prompt affects response quality:
- Vague: "Tell me about AI"
- Specific: "Explain machine learning in 3 sentences for a beginner"

### Temperature
Controls how creative the AI is:
- 0.1: Very focused, predictable, factual
- 0.7: Balanced (default)
- 0.9: Very creative, might be less accurate

### Tokens
Tokens are pieces of text. The model generates responses token-by-token. More tokens = longer text.

### Streaming
Instead of waiting for the complete response, streaming shows text as it's generated. This feels faster to users.

## Web Interface Modules

### User Interface Features

The web interface includes several professional enhancements for an optimal learning experience:

**Visual Design:**
- **Professional Teal/Cyan Color Scheme**: Modern, tech-forward appearance with calming colors
- **Responsive Layout**: Adapts seamlessly to different screen sizes
- **Dark Theme**: Reduced eye strain during extended learning sessions

**Interactive Elements:**
- **33 Custom Tooltips**: Hover over any button or navigation link to see helpful descriptions
  - Navigation links explain each module's purpose
  - Buttons describe their exact function
  - Tooltips appear below the cursor for easy visibility
- **Resizable Text Boxes**: Both prompt inputs and response outputs can be resized
  - Drag horizontally to adjust width
  - Drag vertically to adjust height
  - Drag diagonally to resize both dimensions simultaneously
- **Spacious Input/Output Areas**: Larger textareas and response boxes for comfortable reading and writing

### 1. Basic Requests
Learn to send simple prompts and get responses. Adjust model and temperature to see how they affect output.

### 2. Streaming
See responses generated in real-time. Streaming makes the interface feel more responsive.

### 3. Chat
Have multi-turn conversations where the AI remembers context from previous messages.

### 4. Prompt Engineering
Compare vague prompts with specific, well-written prompts. See how better prompts get better results.

### 5. Advanced
Test different temperature settings, compare models, and control response length.

## Troubleshooting

### Problem: "Connection refused" when running scripts

Solution: Make sure Ollama server is running:
```bash
ollama serve
```

### Problem: "Model not found" error

Solution: Download the model first:
```bash
ollama pull neural-chat
```

### Problem: Flask app won't start

Solution: Check if port 5001 is in use, or another port is blocked:
```bash
# Try a different port by editing app.py
# Change: app.run(debug=True, host="0.0.0.0", port=5001)
# To: app.run(debug=True, host="0.0.0.0", port=5002)
```

### Problem: Slow responses or crashes

Solution: Your computer might not have enough memory:
1. Close other applications
2. Use a smaller model: `ollama pull mistral`
3. Check available RAM

### Problem: Virtual environment not activating

Solution: Make sure you're in the project directory and use the correct activation command:
- macOS/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

### Problem: Response shows "ipynb" or empty response

Solution: This might be a browser issue:
1. Clear browser cache and refresh
2. Try a different browser
3. Make sure Ollama server is running: `ollama serve`
4. Check browser console for errors (F12)

## API Reference

All requests go to: http://localhost:11434

### Generate Endpoint
```
POST /api/generate

Request:
{
  "model": "neural-chat",
  "prompt": "What is Python?",
  "stream": false,
  "temperature": 0.7
}

Response:
{
  "response": "Python is...",
  "eval_count": 42,
  "total_duration": 1234567890
}
```

### Get Available Models
```
GET /api/tags

Response:
{
  "models": [
    {"name": "neural-chat:latest", "size": 3830000000},
    {"name": "mistral:latest", "size": 4070000000}
  ]
}
```

## Next Steps After Learning

1. Build a Chatbot using the chat example
2. Integrate with Apps: Add Ollama to your own applications
3. Try Other Models: Download and experiment with different models
4. Deploy: Host your app on a server using Heroku or AWS
5. Advanced: Learn about prompt engineering and model fine-tuning

## Resources

- Ollama GitHub: https://github.com/ollama/ollama
- Ollama Models: https://ollama.ai/library
- Python Requests Library: https://docs.python-requests.org/
- Flask Documentation: https://flask.palletsprojects.com/

## Getting Help

If you encounter issues:

1. Check the Troubleshooting section above
2. Review the example scripts for reference
3. Visit Ollama's GitHub issues: https://github.com/ollama/ollama/issues
4. Check Flask documentation for web interface issues

## License

This learning project is free to use and modify for educational purposes.

Happy learning!
