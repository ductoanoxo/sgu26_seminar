from dotenv import load_dotenv
import os
import inspect
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_user_prompt(method):

    source_code = inspect.getsource(method)

    return f"""
Generate a Google-style docstring for the following Python method.

CODE:
{source_code}

DOCSTRING:
"""


SYSTEM_PROMPT = """
You are a senior Python developer.
Write a Google-style docstring.
Return docstring only.
"""


if __name__ == "__main__":

    prompt = get_user_prompt(Singleton.__call__)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
    )

    print("\nGenerated Docstring:\n")
    print(completion.choices[0].message.content)