"""
Streaming Response Example
===========================
Instead of waiting for the complete response, get responses in real-time chunks.
This makes it feel faster and more interactive!

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2 (to download the model)
"""

import requests
import json

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "neural-chat"  # Try: mistral, openchat, llama3.2


def streaming_request(prompt, model=MODEL):
    """
    Send a request to Ollama and stream the response in real-time.
    
    Args:
        prompt (str): Your question or instruction
        model (str): The model to use
    
    Yields:
        str: Chunks of the response as they're generated
    """
    
    # Prepare the request payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True  # Enable streaming
    }
    
    print(f"🤔 Thinking...")
    print("-" * 60)
    
    try:
        # Make the streaming request
        response = requests.post(OLLAMA_API, json=payload, stream=True)
        response.raise_for_status()
        
        # Process the streamed response
        for line in response.iter_lines():
            if line:
                try:
                    # Each line is a JSON object
                    json_response = json.loads(line)
                    
                    # Extract the token/text piece
                    token = json_response.get("response", "")
                    
                    # Print without newline for streaming effect
                    print(token, end="", flush=True)
                    
                    # Check if this is the last chunk
                    if json_response.get("done", False):
                        print("\n" + "-" * 60)
                        # Print final stats
                        print(f"✅ Complete!")
                        print(f"   Tokens: {json_response.get('eval_count', 'N/A')}")
                        print(f"   Duration: {json_response.get('total_duration', 'N/A')} ns")
                        
                except json.JSONDecodeError:
                    pass
                    
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to Ollama API")
        print("   Make sure to run: ollama serve")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")


def streaming_with_parameters(prompt, model=MODEL, temperature=0.7, top_p=0.9):
    """
    Streaming request with advanced parameters.
    
    Args:
        prompt (str): Your question or instruction
        model (str): The model to use
        temperature (float): Higher = more creative (0.0-1.0)
        top_p (float): Nucleus sampling parameter
    """
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": True,
        "temperature": temperature,  # Creativity level
        "top_p": top_p  # Diversity control
    }
    
    print(f"🤖 Model: {model} | 🌡️ Temperature: {temperature} | 📊 Top-p: {top_p}")
    print("-" * 60)
    
    try:
        response = requests.post(OLLAMA_API, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    json_response = json.loads(line)
                    token = json_response.get("response", "")
                    print(token, end="", flush=True)
                    
                    if json_response.get("done", False):
                        print("\n" + "-" * 60)
                except json.JSONDecodeError:
                    pass
                    
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Run: ollama serve")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function to demonstrate streaming."""
    
    print("=" * 60)
    print("OLLAMA - STREAMING RESPONSE EXAMPLE")
    print("=" * 60)
    print()
    
    # Example 1: Basic streaming
    print("📌 Example 1: Basic Streaming")
    print()
    prompt1 = "Tell me an interesting fact about Python programming"
    streaming_request(prompt1)
    
    print("\n\n")
    
    # Example 2: Different model (if you have it)
    print("📌 Example 2: Streaming with Parameters")
    print()
    prompt2 = "Write a short creative story about a robot"
    streaming_with_parameters(
        prompt2,
        model=MODEL,
        temperature=0.9,  # Very creative
        top_p=0.95
    )
    
    print("\n\n")
    
    # Example 3: Low temperature (deterministic)
    print("📌 Example 3: Deterministic Response (Low Temperature)")
    print()
    prompt3 = "What is the capital of France?"
    streaming_with_parameters(
        prompt3,
        model=MODEL,
        temperature=0.1,  # Very deterministic
        top_p=0.5
    )


if __name__ == "__main__":
    main()
