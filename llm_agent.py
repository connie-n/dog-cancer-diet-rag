import os
from redis_cache import get_cached_response, set_cached_response
from dotenv import load_dotenv
from openai import OpenAI
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_answer(query, docs):
    context = "\n\n".join([f"[Source: {doc['id']}]\n{doc['content']}" for doc in docs])

    prompt = (
        "Use only the following context to answer the question.\n"
        "Do not make up any facts.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        "Answer:"
    )

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )

    answer = ""
    for event in response:
        if event.type == "response.output_text.delta":
            answer += event.delta
        elif event.type == "response.output_text.done":
            break  

    return answer.strip()


def generate_answer_with_cache(query, docs):
    cached = get_cached_response(query)
    if cached:
        return cached

    answer = generate_answer(query, docs)
    
    set_cached_response(query, answer)
    return answer