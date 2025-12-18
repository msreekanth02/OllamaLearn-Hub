"""
Basic Request Example
=====================
This is the simplest way to interact with Ollama.
It sends a single prompt and gets back a complete response.

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2 (to download the model)
"""

import requests
import json

# Configuration
OLLAMA_API = "http://localhost:11434/api/generate"
MODEL = "neural-chat"  # You can also try: mistral, llama3.2, etc.

def format_response(text, max_width=70):
    """Format response text with proper wrapping."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if sum(len(w) for w in current_line) + len(current_line) + len(word) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(" ".join(current_line))
    
    return lines


def print_box(lines, box_char="│", max_width=70):
    """Print text in a nicely formatted box."""
    print("╔" + "═" * (max_width + 2) + "╗")
    for line in lines:
        padding = max_width - len(line)
        print(f"{box_char} {line}{' ' * padding} {box_char}")
    print("╚" + "═" * (max_width + 2) + "╝")


def simple_request(prompt):
    """
    Send a simple request to Ollama and get the full response.
    
    Args:
        prompt (str): Your question or instruction
    
    Returns:
        str: The model's response
    """
    
    # Prepare the request payload
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False  # Get complete response at once
    }
    
    print(f"\n  🤔 Processing with {MODEL}...")
    print("  ⏳ Please wait...\n")
    
    try:
        # Make the request
        response = requests.post(OLLAMA_API, json=payload)
        response.raise_for_status()  # Raise error if request failed
        
        # Parse the response
        result = response.json()
        
        # Extract the generated text
        generated_text = result.get("response", "").strip()
        
        # Calculate stats
        tokens = result.get('eval_count', 0)
        duration_ns = result.get('total_duration', 0)
        duration_s = duration_ns / 1_000_000_000 if duration_ns else 0
        
        # Print stats with nice formatting
        print("  ✅ Response Generated Successfully!")
        print(f"  📊 Tokens: {tokens}")
        print(f"  ⚡ Speed: {duration_s:.2f}s")
        if duration_s > 0:
            print(f"  🚀 Speed: {tokens/duration_s:.1f} tokens/sec")
        print()
        
        return generated_text
        
    except requests.exceptions.ConnectionError:
        print("  ❌ Connection Error!")
        print("  ⚠️  Cannot connect to Ollama API")
        print("  💡 Make sure to run: ollama serve")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Error: {e}")
        return None


def main():
    """Main function to demonstrate basic request."""
    
    # Header
    print("\n")
    print("  " + "█" * 66)
    print("  █" + " " * 64 + "█")
    print("  █" + "  🤖 OLLAMA - BASIC REQUEST EXAMPLE".center(64) + "█")
    print("  █" + " " * 64 + "█")
    print("  " + "█" * 66)
    
    # Example 1: Simple question
    print("\n  " + "▸" * 33)
    print("  ▸ 📌 EXAMPLE 1: Simple Question")
    print("  " + "▸" * 33)
    prompt1 = "What is machine learning? Explain in 2-3 sentences."
    print(f"\n  ❓ Question: {prompt1}\n")
    response1 = simple_request(prompt1)
    if response1:
        print("  📝 Answer:")
        lines1 = format_response(response1, 64)
        print_box(lines1)
    
    # Example 2: Different question
    print("\n  " + "▸" * 33)
    print("  ▸ 📌 EXAMPLE 2: Creative Writing")
    print("  " + "▸" * 33)
    prompt2 = "Write a haiku about programming"
    print(f"\n  ❓ Request: {prompt2}\n")
    response2 = simple_request(prompt2)
    if response2:
        print("  🎨 Result:")
        lines2 = format_response(response2, 64)
        print_box(lines2)
    
    # Example 3: Code generation
    print("\n  " + "▸" * 33)
    print("  ▸ 📌 EXAMPLE 3: Code Generation")
    print("  " + "▸" * 33)
    prompt3 = "Write a Python function to reverse a string"
    print(f"\n  ❓ Request: {prompt3}\n")
    response3 = simple_request(prompt3)
    if response3:
        print("  💻 Code:")
        lines3 = format_response(response3, 64)
        print_box(lines3)
    
    # Footer
    print("\n  " + "█" * 66)
    print("  █" + " " * 64 + "█")
    print("  █" + "  ✅ All Examples Completed!".center(64) + "█")
    print("  █" + " " * 64 + "█")
    print("  " + "█" * 66)
    print()


if __name__ == "__main__":
    main()
