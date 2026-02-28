import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMManager:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama3-8b-8192"
        try:
            self.client = Groq(api_key=self.api_key) if self.api_key else None
        except:
            self.client = None

    def generate_follow_up(self, fragment):
        """Generates a 'Deep Exploration' question based on the best fragment."""
        if not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "your_groq_api_key_here":
            return "Molecular analysis complete. (Connect a valid Groq API key to enable Deep Exploration AI questions)."

        prompt = f"Based on the following technical fragment from a bakery/pastry ingredient sheet, generate one thought-provoking 'Deep Exploration' question to help the user learn more. Keep it concise:\n\n{fragment}"
        
        try:
            if not self.client:
                raise ValueError("No client")

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are KnowledgeQuest AI, an expert in bakery and pastry science."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {e}")
            # --- DEMO FALLBACK: LAB SIMULATION QUESTION ---
            # If the API fails, we provide a high-quality simulated technical question for the demo.
            fallback_questions = [
                "🔬 LAB SIMULATION: Based on this fragment, what is the optimal hydration percentage required to fully activate the enzyme complex?",
                "🔬 LAB SIMULATION: How would a temperature increase of 5°C during the proofing stage impact the stability of this formulation?",
                "🔬 LAB SIMULATION: Given these ingredients, how would the cross-linking profile change if the pH was adjusted to 5.5?"
            ]
            import random
            return random.choice(fallback_questions)

    def expand_query(self, query):
        """Optional: Can be used to refine user queries."""
        # For now, we mainly use it for follow-ups as per brief.
        pass
