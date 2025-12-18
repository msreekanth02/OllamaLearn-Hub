"""
Conversation / Chat Example
=============================
Maintain conversation history for multi-turn interactions.
This demonstrates how to build a simple chatbot with context awareness.

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2 (to download the model)
"""

import requests
import json


class OllamaChatbot:
    """Simple chatbot that maintains conversation history."""
    
    def __init__(self, model="neural-chat", api_url="http://localhost:11434/api/generate"):
        """
        Initialize the chatbot.
        
        Args:
            model (str): The model to use
            api_url (str): The Ollama API endpoint
        """
        self.model = model
        self.api_url = api_url
        self.conversation_history = []
        self.system_prompt = "You are a helpful assistant. Provide clear and concise answers."
    
    def set_system_prompt(self, prompt):
        """Set the system prompt (personality/behavior)."""
        self.system_prompt = prompt
    
    def build_prompt(self, user_message):
        """
        Build the full prompt including conversation history.
        
        Args:
            user_message (str): The latest user message
            
        Returns:
            str: The complete prompt with history
        """
        # Start with system prompt
        full_prompt = f"System: {self.system_prompt}\n\n"
        
        # Add conversation history
        for exchange in self.conversation_history:
            full_prompt += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n\n"
        
        # Add current user message
        full_prompt += f"User: {user_message}\nAssistant:"
        
        return full_prompt
    
    def chat(self, user_message, stream=True):
        """
        Send a message and get a response (maintaining history).
        
        Args:
            user_message (str): The user's input
            stream (bool): Whether to stream the response
            
        Returns:
            str: The assistant's response
        """
        
        # Build the full prompt with history
        full_prompt = self.build_prompt(user_message)
        
        # Prepare payload
        payload = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": stream,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(self.api_url, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                # Collect streamed response
                full_response = ""
                print("💬 ", end="", flush=True)
                
                for line in response.iter_lines():
                    if line:
                        try:
                            json_resp = json.loads(line)
                            token = json_resp.get("response", "")
                            print(token, end="", flush=True)
                            full_response += token
                        except json.JSONDecodeError:
                            pass
                
                print()  # New line after streaming
                
            else:
                # Get complete response at once
                result = response.json()
                full_response = result.get("response", "")
                print(f"💬 {full_response}")
            
            # Add to conversation history
            self.conversation_history.append({
                "user": user_message,
                "assistant": full_response.strip()
            })
            
            return full_response
            
        except requests.exceptions.ConnectionError:
            print("❌ Error: Cannot connect to Ollama API")
            print("   Make sure to run: ollama serve")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        print("🗑️  Conversation history cleared")
    
    def show_history(self):
        """Display the conversation history."""
        print("\n📋 Conversation History:")
        print("-" * 60)
        
        if not self.conversation_history:
            print("(No conversation history yet)")
            return
        
        for i, exchange in enumerate(self.conversation_history, 1):
            print(f"\n[Exchange {i}]")
            print(f"👤 User: {exchange['user']}")
            print(f"🤖 Assistant: {exchange['assistant'][:100]}...")  # Show first 100 chars
        
        print("\n" + "-" * 60)


def interactive_chat():
    """Interactive chat mode (command line)."""
    
    print("=" * 60)
    print("OLLAMA - INTERACTIVE CHATBOT")
    print("=" * 60)
    print()
    
    # Initialize chatbot
    bot = OllamaChatbot(model="llama2")
    
    print(f"🤖 Chatbot initialized with model: {bot.model}")
    print("💬 Type 'quit' to exit")
    print("📋 Type 'history' to see conversation history")
    print("🗑️  Type 'clear' to clear history")
    print("-" * 60)
    print()
    
    while True:
        # Get user input
        try:
            user_input = input("You: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Handle special commands
        if user_input.lower() == "quit":
            print("👋 Goodbye!")
            break
        elif user_input.lower() == "history":
            bot.show_history()
            continue
        elif user_input.lower() == "clear":
            bot.clear_history()
            continue
        
        # Send message and get response
        bot.chat(user_input, stream=True)
        print()


def demo_conversation():
    """Demonstrate a pre-scripted conversation."""
    
    print("=" * 60)
    print("OLLAMA - CONVERSATION DEMO")
    print("=" * 60)
    print()
    
    # Create chatbot with custom system prompt
    bot = OllamaChatbot(model="llama2")
    bot.set_system_prompt("You are a friendly Python programming tutor. Explain concepts clearly.")
    
    # Pre-scripted conversation
    questions = [
        "What is a list in Python?",
        "How do I add elements to a list?",
        "What's the difference between a list and a tuple?",
        "Can you give me an example of using a list?"
    ]
    
    print(f"🤖 Model: {bot.model}")
    print(f"📚 System Prompt: {bot.system_prompt}")
    print("-" * 60)
    print()
    
    for question in questions:
        print(f"👤 User: {question}")
        bot.chat(question, stream=True)
        print()
    
    # Show the full conversation
    bot.show_history()


def main():
    """Main function."""
    
    # Uncomment one of the following:
    
    # Run interactive chat mode
    interactive_chat()
    
    # Or run demo conversation
    # demo_conversation()


if __name__ == "__main__":
    main()
