import os
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
        
    )

    answer = response.output[0].content[0].text.strip()
    return answer
