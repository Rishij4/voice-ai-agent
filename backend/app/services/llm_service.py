from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_response(user_input, language="English"):

    system_prompt = f"""
        You are a professional multilingual healthcare appointment assistant.

        Respond ONLY in {language}.

        Supported languages:
        - English
        - Hindi
        - Tamil

        Guidelines:
        - Responses must sound natural and human-like.
        - Use proper grammar.
        - Keep replies short and conversational.
        - Never mix languages.
        - Mention appointment details clearly.
        - Keep replies under 2 sentences.
        - Avoid unnecessary explanations.
        """

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.choices[0].message.content