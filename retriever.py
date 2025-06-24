from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.config import Settings
import os


model = SentenceTransformer("all-MiniLM-L6-v2")
client = PersistentClient(path="vector_store")
collection = client.get_or_create_collection("dog_cancer_docs")

def retrieve_similar_docs(query: str, top_k: int = 2):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=['documents']
    )

    docs = []
    for i in range(top_k):
        docs.append({
            "id": results['ids'][0][i],
            "content": results['documents'][0][i]
        })
        
    return docs


def load_texts_from_dir(txt_dir):
    documents = []
    for fname in os.listdir(txt_dir):
        if fname.endswith(".txt"):
            with open(os.path.join(txt_dir, fname), "r", encoding="utf-8") as f:
                text = f.read()
                documents.append({"id": fname, "content": text})
            
    return documents



def store_embeddings_chroma(txt_dir="data/mock_data"):
    
    docs = load_texts_from_dir(txt_dir)

    #client = PersistentClient(path=persist_dir)
    #collection = client.get_or_create_collection("dog_cancer_docs")

    for doc in docs:
        embedding = model.encode(doc["content"])
        collection.add(
            documents=[doc["content"]],
            embeddings=[embedding.tolist()],
            ids=[doc["id"]]
        )
    #client.persist()
    
    print("Embeddings stored in ChromaDB")


if __name__ == "__main__":
    store_embeddings_chroma()

