import openai
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    client: OpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=2,
        max_tokens=100,
        n=3,
        messages=[
            {"role": "system", "content": "You are a hiring manager at a tech company."},
            {"role": "user", "content": "What is the Two Sum problem?"}
        ]
    )

    print("Completion Tokens:", completion.usage.completion_tokens)

    print("\nOutput 1:", completion.choices[0].message.content)
    print("\nOutput 2:", completion.choices[1].message.content)
    print("\nOutput 3:", completion.choices[2].message.content)

    print("\nToken usage:")
    print("Prompt tokens:", completion.usage.prompt_tokens)
    print("Completion tokens:", completion.usage.completion_tokens)
    print("Total tokens:", completion.usage.total_tokens)