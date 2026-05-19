import os
from dotenv import load_dotenv
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def router_question(question):
    prompt = f"""
    You are a query router for a multi-document research assistant.

    The uploaded papers may include topics like YOLO, Transformers, BERT, CLIP, Segment Anything, U-Net, ResNet, or other research papers.

    Decide whether the user's question should search uploaded research papers.

    Return only one word:
    RAG - if the question asks about a topic likely covered by uploaded papers, including YOLO, Transformer, BERT, CLIP, Segment Anything, U-Net, ResNet, paper methods, results, authors, limitations, comparisons, or citations.
    GENERAL - if the question is broad learning help and does not need uploaded paper content.

    Examples:
    Question: What is YOLO?
    Route: RAG

    Question: What is self-attention?
    Route: RAG

    Question: Compare YOLO and Transformers.
    Route: RAG

    Question: What is machine learning?
    Route: GENERAL

    Question: How do I prepare for an AI interview?
    Route: GENERAL

    Question:
    {question}
    """

    response=client.chat.completions.create(
        model=os.getenv("GROQ_MODEL","llama-3.1-8b-instant"),
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0,
        max_tokens=10
    )
    route=response.choices[0].message.content.strip().upper()
    rag_keywords = [
        "yolo", "transformer", "bert", "clip",
        "segment anything", "u-net", "unet", "resnet",
        "paper", "papers", "citation", "according to"
    ]

    if any(keyword in question.lower() for keyword in rag_keywords):
        return "RAG"
    if "RAG" in route:
        return "RAG"
    else:
        return "GENERAL"