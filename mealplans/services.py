import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class OpenAIService:
    @staticmethod
    def generate_meal_plan(preferences: str, calories: int = None) -> str:
        """
        Stub for meal plan generation. Call GPT-4 with a prompt based on user preferences.
        Returns the text of the generated meal plan.
        """
        prompt = f"Create a clean-eating meal plan" \
                 f" with the following preferences: {preferences}."
        if calories:
            prompt += f" Total daily calories: {calories}."

        # This is a stub: you can expand with fine-tuned parameters
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a healthy meal planner."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            n=1,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()