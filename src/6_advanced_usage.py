"""
Advanced Usage & Configuration
================================
Learn advanced features like custom parameters, error handling,
model comparisons, and optimization techniques.

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2 (or other models)
"""

import requests
import json
import time
from typing import Dict, Any


class AdvancedOllama:
    """Advanced Ollama usage patterns."""
    
    def __init__(self, host: str = "http://localhost:11434"):
        self.host = host
        self.api_url = f"{host}/api/generate"
        self.models_url = f"{host}/api/tags"
    
    # ============= PARAMETER TUNING =============
    
    def generate_with_parameters(self, prompt: str, model: str = "llama2", 
                                 **params) -> Dict[str, Any]:
        """
        Generate with fine-tuned parameters.
        
        Args:
            prompt (str): The prompt
            model (str): Model name
            **params: Additional parameters:
                - temperature: float (0-1, default 0.7)
                - top_p: float (0-1, default 0.9)
                - top_k: int (default 40)
                - repeat_penalty: float (default 1.1)
                - num_predict: int (output tokens)
                - num_ctx: int (context window)
        """
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            **params
        }
        
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def creative_mode(self, prompt: str, model: str = "llama2") -> str:
        """Generate creative output with high temperature."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            temperature=0.9,      # High creativity
            top_p=0.95,          # High diversity
            top_k=50
        )
        
        return result.get("response", "")
    
    def precise_mode(self, prompt: str, model: str = "llama2") -> str:
        """Generate factual, deterministic output."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            temperature=0.1,      # Low creativity
            top_p=0.5,           # Low diversity
            top_k=10
        )
        
        return result.get("response", "")
    
    def balanced_mode(self, prompt: str, model: str = "llama2") -> str:
        """Balanced creative and factual output."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            temperature=0.7,      # Balanced
            top_p=0.9,           # Balanced
            top_k=40
        )
        
        return result.get("response", "")
    
    # ============= CONTROL OUTPUT LENGTH =============
    
    def short_response(self, prompt: str, model: str = "llama2") -> str:
        """Generate a short response."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            num_predict=50  # Limit to 50 tokens
        )
        
        return result.get("response", "")
    
    def long_response(self, prompt: str, model: str = "llama2") -> str:
        """Generate a longer response."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            num_predict=500  # Allow up to 500 tokens
        )
        
        return result.get("response", "")
    
    # ============= MODEL INFORMATION =============
    
    def list_models(self) -> list:
        """Get list of available models."""
        
        try:
            response = requests.get(self.models_url)
            response.raise_for_status()
            
            models = response.json().get("models", [])
            return models
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_model_info(self, model_name: str) -> Dict:
        """Get information about a specific model."""
        
        models = self.list_models()
        
        for model in models:
            if model_name in model.get("name", ""):
                return model
        
        return {}
    
    # ============= BENCHMARKING =============
    
    def benchmark_models(self, prompt: str, models: list = None) -> Dict:
        """Compare response time across models."""
        
        if models is None:
            available_models = self.list_models()
            models = [m["name"] for m in available_models][:3]  # Test first 3
        
        results = {}
        
        print(f"🏃 Benchmarking {len(models)} models...")
        print("-" * 70)
        
        for model_name in models:
            print(f"Testing {model_name}...", end=" ", flush=True)
            
            try:
                start_time = time.time()
                
                response = requests.post(self.api_url, json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False
                })
                
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    results[model_name] = {
                        "time": elapsed,
                        "tokens": data.get("eval_count", 0),
                        "status": "✅"
                    }
                    print(f"✅ {elapsed:.2f}s ({data.get('eval_count', 0)} tokens)")
                else:
                    results[model_name] = {
                        "time": None,
                        "status": f"❌ Error {response.status_code}"
                    }
                    print(f"❌ Error")
                    
            except Exception as e:
                results[model_name] = {
                    "time": None,
                    "status": f"❌ {str(e)}"
                }
                print(f"❌ {str(e)}")
        
        print("-" * 70)
        return results
    
    # ============= ERROR HANDLING =============
    
    def safe_generate(self, prompt: str, model: str = "llama2", 
                     max_retries: int = 3) -> str:
        """Generate with retry logic."""
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries}...", end=" ")
                
                response = requests.post(
                    self.api_url,
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False
                    },
                    timeout=30
                )
                
                response.raise_for_status()
                print("✅")
                return response.json().get("response", "")
                
            except requests.exceptions.Timeout:
                print("⏱️ Timeout")
                if attempt < max_retries - 1:
                    time.sleep(2)
                continue
                
            except requests.exceptions.ConnectionError:
                print("❌ Connection error")
                if attempt < max_retries - 1:
                    time.sleep(2)
                continue
                
            except Exception as e:
                print(f"❌ {e}")
                break
        
        return "Failed to generate response after retries"
    
    # ============= CONTEXT WINDOW =============
    
    def with_large_context(self, prompt: str, model: str = "llama2") -> str:
        """Use larger context window (if model supports it)."""
        
        result = self.generate_with_parameters(
            prompt,
            model=model,
            num_ctx=4096  # Larger context
        )
        
        return result.get("response", "")
    
    # ============= ADVANCED PROMPTING =============
    
    def structured_output(self, prompt: str, format_spec: str, 
                         model: str = "llama2") -> str:
        """Generate structured output (JSON, CSV, etc.)."""
        
        enhanced_prompt = f"""{prompt}

Format your response as: {format_spec}
Ensure the output is valid and properly formatted."""
        
        result = self.generate_with_parameters(
            enhanced_prompt,
            model=model,
            temperature=0.1  # Low temperature for structured data
        )
        
        return result.get("response", "")


def demo_parameter_tuning():
    """Demonstrate parameter tuning effects."""
    
    print("\n" + "=" * 70)
    print("PARAMETER TUNING DEMONSTRATION")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    prompt = "Tell me an interesting fact about space"
    
    print("🎭 CREATIVE MODE (high temperature)")
    print("-" * 70)
    print(engine.creative_mode(prompt)[:200] + "...\n")
    
    print("📚 PRECISE MODE (low temperature)")
    print("-" * 70)
    print(engine.precise_mode(prompt)[:200] + "...\n")
    
    print("⚖️  BALANCED MODE")
    print("-" * 70)
    print(engine.balanced_mode(prompt)[:200] + "...\n")


def demo_output_length():
    """Demonstrate output length control."""
    
    print("=" * 70)
    print("OUTPUT LENGTH CONTROL")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    prompt = "Tell me about machine learning"
    
    print("📄 SHORT RESPONSE (50 tokens max)")
    print("-" * 70)
    print(engine.short_response(prompt) + "\n")
    
    print("📖 LONG RESPONSE (500 tokens max)")
    print("-" * 70)
    response = engine.long_response(prompt)
    print(response[:300] + ("..." if len(response) > 300 else "") + "\n")


def demo_model_info():
    """Display available models."""
    
    print("=" * 70)
    print("AVAILABLE MODELS")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    models = engine.list_models()
    
    if not models:
        print("No models found. Run: ollama pull llama2")
        return
    
    print(f"📋 Found {len(models)} model(s):\n")
    
    for model in models:
        name = model.get("name", "Unknown")
        size = model.get("size", 0)
        size_gb = size / (1024**3)
        
        print(f"   • {name}")
        print(f"     Size: {size_gb:.2f} GB")
        print()


def demo_benchmarking():
    """Compare model performance."""
    
    print("=" * 70)
    print("MODEL BENCHMARKING")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    prompt = "What is Python programming?"
    
    results = engine.benchmark_models(prompt)
    
    print("\n📊 Benchmark Results:")
    print("-" * 70)
    
    for model, stats in results.items():
        print(f"\n{model}:")
        print(f"  Status: {stats.get('status')}")
        if stats.get('time'):
            print(f"  Response Time: {stats['time']:.2f}s")
            print(f"  Tokens: {stats.get('tokens', 0)}")


def demo_error_handling():
    """Demonstrate error handling."""
    
    print("\n" + "=" * 70)
    print("ERROR HANDLING WITH RETRIES")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    print("🔄 Attempting to generate with retry logic...")
    response = engine.safe_generate("What is AI?", max_retries=3)
    print(f"\nResponse:\n{response[:200]}...\n")


def demo_structured_output():
    """Demonstrate structured output generation."""
    
    print("=" * 70)
    print("STRUCTURED OUTPUT")
    print("=" * 70 + "\n")
    
    engine = AdvancedOllama()
    
    print("📋 JSON Output Example")
    print("-" * 70)
    
    prompt = "List 3 fruits with their colors"
    output = engine.structured_output(
        prompt,
        format_spec='{"fruits": [{"name": "...", "color": "..."}]}'
    )
    print(output)


def main():
    """Run all demonstrations."""
    
    print("\n" + "=" * 70)
    print("ADVANCED OLLAMA USAGE")
    print("=" * 70)
    
    demo_parameter_tuning()
    demo_output_length()
    demo_model_info()
    demo_benchmarking()
    demo_error_handling()
    demo_structured_output()


if __name__ == "__main__":
    main()
