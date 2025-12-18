"""
Ollama Python SDK / Library Example
====================================
Using higher-level libraries to interact with Ollama makes code cleaner.

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2
- Install: pip install ollama
"""

import json
from typing import Optional, List


# Note: If you don't have the ollama package installed, run:
# pip install ollama

try:
    from ollama import Client, generate
    OLLAMA_INSTALLED = True
except ImportError:
    OLLAMA_INSTALLED = False
    print("Note: ollama package not installed. Using requests fallback.")
    import requests


class OllamaSDK:
    """Wrapper class for Ollama SDK."""
    
    def __init__(self, host: str = "http://localhost:11434", model: str = "llama2"):
        """
        Initialize Ollama client.
        
        Args:
            host (str): Ollama server URL
            model (str): Default model to use
        """
        self.model = model
        self.host = host
        
        if OLLAMA_INSTALLED:
            self.client = Client(host=host)
        else:
            self.client = None
    
    def simple_generate(self, prompt: str) -> str:
        """
        Generate text from a prompt using SDK.
        
        Args:
            prompt (str): The input prompt
            
        Returns:
            str: Generated text
        """
        if not OLLAMA_INSTALLED:
            return self._fallback_generate(prompt)
        
        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=False,
            )
            return response['response']
        except Exception as e:
            return f"Error: {e}"
    
    def streaming_generate(self, prompt: str):
        """
        Generate text with streaming.
        
        Args:
            prompt (str): The input prompt
            
        Yields:
            str: Text chunks
        """
        if not OLLAMA_INSTALLED:
            print("SDK not available. Run: pip install ollama")
            return
        
        try:
            print("🤔 Generating... ")
            print("-" * 60)
            
            for chunk in self.client.generate(
                model=self.model,
                prompt=prompt,
                stream=True,
            ):
                print(chunk['response'], end='', flush=True)
            
            print("\n" + "-" * 60)
        except Exception as e:
            print(f"Error: {e}")
    
    def pull_model(self, model_name: str):
        """Download a model."""
        if not OLLAMA_INSTALLED:
            print("SDK not available. Run: pip install ollama")
            return
        
        try:
            print(f"📥 Pulling model: {model_name}")
            for chunk in self.client.pull(model_name, stream=True):
                print(chunk['status'])
        except Exception as e:
            print(f"Error: {e}")
    
    def list_models(self) -> List[str]:
        """List available models."""
        if not OLLAMA_INSTALLED:
            return ["SDK not available"]
        
        try:
            tags = self.client.tags()
            models = [model['name'] for model in tags.get('models', [])]
            return models
        except Exception as e:
            return [f"Error: {e}"]
    
    def _fallback_generate(self, prompt: str) -> str:
        """Fallback to requests if SDK not available."""
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()['response']
        except Exception as e:
            return f"Error: {e}"


def example_1_basic_sdk():
    """Example 1: Basic SDK usage."""
    
    print("=" * 60)
    print("EXAMPLE 1: Basic SDK Usage")
    print("=" * 60)
    print()
    
    sdk = OllamaSDK(model="llama2")
    
    prompt = "What are the three laws of robotics? List them clearly."
    print(f"📝 Prompt: {prompt}\n")
    
    response = sdk.simple_generate(prompt)
    print(f"💬 Response:\n{response}\n")


def example_2_streaming_sdk():
    """Example 2: Streaming with SDK."""
    
    print("=" * 60)
    print("EXAMPLE 2: Streaming with SDK")
    print("=" * 60)
    print()
    
    sdk = OllamaSDK(model="llama2")
    
    prompt = "Write a haiku about artificial intelligence"
    print(f"📝 Prompt: {prompt}\n")
    
    sdk.streaming_generate(prompt)
    print()


def example_3_multiple_models():
    """Example 3: Use different models."""
    
    print("=" * 60)
    print("EXAMPLE 3: Different Models Comparison")
    print("=" * 60)
    print()
    
    prompt = "What is the meaning of life?"
    
    models = ["llama2", "mistral", "neural-chat"]
    
    for model in models:
        print(f"🤖 Model: {model}")
        print("-" * 60)
        
        sdk = OllamaSDK(model=model)
        response = sdk.simple_generate(prompt)
        
        # Show first 200 chars
        preview = response[:200] + "..." if len(response) > 200 else response
        print(f"{preview}\n")


def example_4_list_models():
    """Example 4: List available models."""
    
    print("=" * 60)
    print("EXAMPLE 4: Available Models")
    print("=" * 60)
    print()
    
    sdk = OllamaSDK()
    
    print("📋 Downloaded Models:")
    models = sdk.list_models()
    
    if not models or "Error" in str(models):
        print("   No models found or SDK error")
        print("   Try running: ollama pull llama2")
    else:
        for model in models:
            print(f"   ✓ {model}")
    
    print()


def example_5_batch_processing():
    """Example 5: Process multiple prompts."""
    
    print("=" * 60)
    print("EXAMPLE 5: Batch Processing")
    print("=" * 60)
    print()
    
    sdk = OllamaSDK(model="llama2")
    
    prompts = [
        "What is 2+2?",
        "Capital of France?",
        "Best programming language?"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"[{i}] Question: {prompt}")
        response = sdk.simple_generate(prompt)
        print(f"    Answer: {response.strip()}\n")


def raw_vs_sdk_comparison():
    """Compare raw requests vs SDK approach."""
    
    print("=" * 60)
    print("RAW REQUESTS VS SDK COMPARISON")
    print("=" * 60)
    print()
    
    print("📌 Raw Requests Approach:")
    print("""
    import requests
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": "Hi"}
    )
    text = response.json()['response']
    """)
    
    print("\n📌 SDK Approach:")
    print("""
    from ollama import Client
    client = Client()
    response = client.generate(model="llama2", prompt="Hi")
    text = response['response']
    """)
    
    print("\n✅ SDK Benefits:")
    print("   • Cleaner, more Pythonic syntax")
    print("   • Error handling built-in")
    print("   • Additional features (list_models, pull, etc.)")
    print("   • Type hints and documentation")
    print("   • Easier to use in production code")


def installation_guide():
    """Show how to install Ollama Python package."""
    
    print("=" * 60)
    print("INSTALLATION GUIDE")
    print("=" * 60)
    print()
    
    print("Step 1: Install the ollama package")
    print("   pip install ollama")
    print()
    
    print("Step 2: Make sure Ollama server is running")
    print("   ollama serve")
    print()
    
    print("Step 3: Import and use in your code")
    print("   from ollama import Client")
    print("   client = Client()")
    print("   response = client.generate(model='llama2', prompt='Hello')")
    print()


def main():
    """Run all examples."""
    
    print("\n" + "=" * 60)
    print("OLLAMA PYTHON SDK EXAMPLES")
    print("=" * 60)
    print()
    
    # Check if SDK is installed
    if not OLLAMA_INSTALLED:
        print("⚠️  Ollama Python SDK not installed!")
        print("   Run: pip install ollama")
        installation_guide()
        
        print("\n💡 Using fallback (raw requests) instead...\n")
        example_1_basic_sdk()
    else:
        print("✅ Ollama SDK installed!\n")
        
        example_1_basic_sdk()
        example_2_streaming_sdk()
        example_3_multiple_models()
        example_4_list_models()
        example_5_batch_processing()
    
    raw_vs_sdk_comparison()


if __name__ == "__main__":
    main()
