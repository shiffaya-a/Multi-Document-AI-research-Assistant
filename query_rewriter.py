import os

from click import prompt
from dotenv import load_dotenv
from groq import Groq
from memory import get_memory_text

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def rewrite_question(question):
    memory_text=get_memory_text()
    prompt = f"""
    You are a query rewriting assistant for a research-paper RAG system.

    Rewrite the user's latest question into a clear standalone search query.

    Rules:
    - Use conversation memory to resolve words like it, its, this, that, they.
    - If the previous topic was YOLO and the user says "it", replace "it" with YOLO.
    - If the user asks "where is it used", rewrite it as "What tasks or applications is [topic] used for?"
    - Do not answer the question.
    - Do not explain your reasoning.
    - Return only the rewritten question as one sentence.

    Conversation memory:
    {memory_text}

    Latest question:
    {question}

    Standalone question:
    """

    response=client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
