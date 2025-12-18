"""
Prompt Engineering Example
============================
Learn how to craft better prompts to get better responses from the model.
Small changes in how you ask questions can lead to very different results!

Prerequisites:
- Run: ollama serve (in another terminal)
- Run: ollama pull llama2
"""

import requests
import json


def ask_model(prompt, model="llama2"):
    """
    Send a prompt to Ollama and get the response.
    
    Args:
        prompt (str): The prompt/question
        model (str): The model to use
        
    Returns:
        str: The model's response
    """
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.7
    }
    
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"


def demonstrate_technique(title, prompts, descriptions):
    """Helper function to demonstrate a technique."""
    
    print(f"\n{'=' * 70}")
    print(f"🎯 {title}")
    print(f"{'=' * 70}\n")
    
    for i, (description, prompt) in enumerate(zip(descriptions, prompts), 1):
        print(f"--- Approach {i}: {description} ---")
        print(f"Prompt: {prompt}")
        print("-" * 70)
        
        response = ask_model(prompt)
        
        # Show first 300 characters
        preview = response[:300] + "..." if len(response) > 300 else response
        print(f"Response:\n{preview}\n")


def technique_1_specificity():
    """Technique 1: Being Specific vs. Vague"""
    
    demonstrate_technique(
        "TECHNIQUE 1: SPECIFICITY",
        [
            "Tell me about Python",
            "Write a Python function to calculate the factorial of a number. Include comments explaining each step."
        ],
        [
            "Vague - Generic answer",
            "Specific - Detailed, actionable answer"
        ]
    )


def technique_2_role_playing():
    """Technique 2: Role-Playing / Context Setting"""
    
    demonstrate_technique(
        "TECHNIQUE 2: ROLE-PLAYING",
        [
            "Explain quantum computing",
            "You are a physics professor. Explain quantum computing to a high school student using everyday analogies."
        ],
        [
            "No context - Technical explanation",
            "With role-playing - Tailored to audience"
        ]
    )


def technique_3_examples():
    """Technique 3: Provide Examples"""
    
    demonstrate_technique(
        "TECHNIQUE 3: PROVIDE EXAMPLES",
        [
            "How do I use list comprehensions in Python?",
            "How do I use list comprehensions in Python? Here's an example: squares = [x**2 for x in range(5)]. Can you give me 2 more practical examples?"
        ],
        [
            "Generic explanation",
            "With examples - More concrete and helpful"
        ]
    )


def technique_4_step_by_step():
    """Technique 4: Step-by-Step Thinking"""
    
    demonstrate_technique(
        "TECHNIQUE 4: STEP-BY-STEP",
        [
            "Is the sum of the angles in a triangle always 180 degrees?",
            "Let me think through this step by step. In a triangle, we have three angles. What geometric principles determine the total angle measure? Can you walk me through the proof that they sum to 180 degrees?"
        ],
        [
            "Simple yes/no",
            "Step-by-step reasoning"
        ]
    )


def technique_5_output_format():
    """Technique 5: Specify Output Format"""
    
    demonstrate_technique(
        "TECHNIQUE 5: OUTPUT FORMAT",
        [
            "Tell me the benefits of exercise",
            "Tell me the benefits of exercise. Format your response as a bulleted list with 5 items. Each bullet should be one sentence."
        ],
        [
            "Free-form response",
            "Structured format - Easy to scan"
        ]
    )


def technique_6_constraints():
    """Technique 6: Add Constraints"""
    
    demonstrate_technique(
        "TECHNIQUE 6: CONSTRAINTS",
        [
            "Write a poem about programming",
            "Write a poem about programming in exactly 8 lines. Each line should be about web development, and it should rhyme (AABB pattern)."
        ],
        [
            "Open-ended",
            "With constraints - More focused"
        ]
    )


def technique_7_chain_of_thought():
    """Technique 7: Chain of Thought"""
    
    demonstrate_technique(
        "TECHNIQUE 7: CHAIN OF THOUGHT",
        [
            "Solve: If I have 3 apples and I buy 5 more, then give away 2, how many do I have?",
            "Solve this step by step: If I have 3 apples and I buy 5 more, then give away 2, how many do I have? Show your work for each step."
        ],
        [
            "Direct answer",
            "Chain of thought - Shows reasoning"
        ]
    )


def technique_8_negative_instructions():
    """Technique 8: Negative Instructions (What NOT to do)"""
    
    demonstrate_technique(
        "TECHNIQUE 8: NEGATIVE INSTRUCTIONS",
        [
            "Explain blockchain",
            "Explain blockchain technology. Do NOT use technical jargon. Do NOT talk about cryptocurrency. Keep it simple and beginner-friendly."
        ],
        [
            "Likely technical explanation",
            "Constrained to be beginner-friendly"
        ]
    )


def advanced_prompt_examples():
    """Show advanced prompt engineering patterns."""
    
    print(f"\n{'=' * 70}")
    print("🚀 ADVANCED PATTERNS")
    print(f"{'=' * 70}\n")
    
    advanced_prompts = {
        "Few-Shot Learning": {
            "description": "Provide examples of desired behavior",
            "prompt": """Here are examples of sentiment analysis:
Text: "I love this product!" → Sentiment: Positive
Text: "This is terrible" → Sentiment: Negative
Text: "The weather is cloudy" → Sentiment: ?

Now analyze: "This movie was amazing and I enjoyed every minute!"
Answer:"""
        },
        "Decomposition": {
            "description": "Break complex problem into parts",
            "prompt": """I want to learn machine learning. Break this down for me:
1. What are the prerequisites I need?
2. What are the main areas I should study?
3. What projects should I build?
4. How long will this take?"""
        },
        "Meta Prompting": {
            "description": "Ask the model to improve your prompt",
            "prompt": """My prompt is: "How do I get better at programming?"
This prompt is too vague. Can you suggest a better, more specific version of this prompt that would get better answers?"""
        }
    }
    
    for name, data in advanced_prompts.items():
        print(f"📌 {name}")
        print(f"Description: {data['description']}")
        print(f"Prompt: {data['prompt']}")
        print("-" * 70)
        response = ask_model(data['prompt'])
        preview = response[:250] + "..." if len(response) > 250 else response
        print(f"Response: {preview}\n")


def tips_and_best_practices():
    """Print tips for effective prompting."""
    
    print(f"\n{'=' * 70}")
    print("💡 TIPS & BEST PRACTICES")
    print(f"{'=' * 70}\n")
    
    tips = [
        ("Be Clear & Specific", "The more specific your prompt, the better the response."),
        ("Provide Context", "Give background information that helps the model understand."),
        ("Use Examples", "Showing examples of what you want is very effective."),
        ("Break It Down", "For complex tasks, break them into smaller steps."),
        ("Specify Format", "Tell the model how you want the response formatted."),
        ("Add Constraints", "Specify length, style, tone, or other limitations."),
        ("Use Temperature Wisely", "Low temp (0-0.3): factual. High temp (0.7-1.0): creative."),
        ("Iterate", "If the first response isn't great, refine your prompt and try again."),
        ("Role Play", "Sometimes assigning a role helps the model understand context."),
        ("Ask for Reasoning", "Ask the model to show its thinking process."),
    ]
    
    for i, (tip, explanation) in enumerate(tips, 1):
        print(f"{i}. {tip}")
        print(f"   → {explanation}\n")


def main():
    """Run all examples."""
    
    print("\n" + "=" * 70)
    print("PROMPT ENGINEERING GUIDE")
    print("=" * 70)
    print("\nThis guide shows different techniques to improve your prompts.\n")
    
    # Run techniques
    technique_1_specificity()
    technique_2_role_playing()
    technique_3_examples()
    technique_4_step_by_step()
    technique_5_output_format()
    technique_6_constraints()
    technique_7_chain_of_thought()
    technique_8_negative_instructions()
    
    # Show advanced patterns
    advanced_prompt_examples()
    
    # Show tips
    tips_and_best_practices()
    
    print("=" * 70)
    print("\n✅ End of Prompt Engineering Guide\n")


if __name__ == "__main__":
    main()
