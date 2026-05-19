chat_history=[]
def add_to_memory(question,answer):
    chat_history.append({
        "user":question,
        "assistant":answer
    })

def get_memory_text():
    if not chat_history:
        return "No previous conversation"
    memory_text=""
    for item in chat_history[-5:]:
        memory_text+=f"User:{item["user"]}\n"
        memory_text+=f"Assistant:{item["assistant"]}\n\n"
    return memory_text


add_to_memory(
    "What is YOLO?",
    "YOLO is an object detection model."
)

add_to_memory(
    "Who created Transformers?",
    "The Transformer paper was written by Vaswani and others."
)

print(get_memory_text())
