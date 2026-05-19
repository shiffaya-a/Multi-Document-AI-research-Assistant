import os
from dotenv import load_dotenv
from groq import  Groq
from memory import get_memory_text



load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def create_context_from_results(results):
    context=[]
    documents=results["documents"][0]
    metadatas=results["metadatas"][0]
    for i, document in enumerate(documents,start=1):
        metadata=metadatas[i-1]
        source=metadata["source"]
        page=metadata["page_number"]
        context.append(
            f"[{i}] Source :{source},page :{page}\n{document}"
        )
    return "\n\n".join(context)

def generate_answer(question,results):
    context=create_context_from_results(results)
    memory_text=get_memory_text()

    prompt = f"""
    You are a research assistant.

    Answer the user's question using only the context below.
    If the answer is not in the context, say you do not know.
    Use simple language.
    Mention citations like [1], [2] when you use information.
    Conversation memory:
    {memory_text}

    Context:
    {context}

    Question:
    {question}
    """
    response=client.chat.completions.create(
        model=os.getenv("GROQ_MODEL","llama-3.1-8b-instant"),
        messages=[
            {'role':'user',
            'content':prompt}
        ],
        temperature=0.2,
        max_tokens= 500
    )
    return response.choices[0].message.content

def generate_general_answer(question):
    prompt = f"""
You are a helpful AI research tutor.

Answer the user's question clearly and simply.
Do not cite uploaded papers because this is a general knowledge answer.

Question:
{question}
"""

    response = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content