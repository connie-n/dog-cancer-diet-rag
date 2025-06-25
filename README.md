# dog-cancer-diet-rag
After reviewing the assignment prompt, I built a demo application focused on answering the question:
"What kinds of food are beneficial for dogs with cancer?"

The core idea of this project was to test whether a small autonomous LLM agent could retrieve specific recipes and generate helpful, grounded answers. To do this, I created mock documents containing recipes and nutritional research tailored for dogs with cancer. I then tested whether the system could accurately surface relevant documents and generate structured responses based on them.

This project is designed to be lightweight, testable, and easy to run with mock data. If you encounter any issues or have additional questions, feel free to reach out — I’d be happy to clarify.

All core functionalities requested in the assignment have been implemented, and further details on system components and bonus features can be found below in the documentation.


## Summary
- FastAPI Endpoint
Implemented in `main.py`, this endpoint accepts a JSON-formatted query and returns a structured response. The response includes an `answer` field and a list of `sources` indicating the documents used for grounding.

- Context Retrieval
This is handled via a local embedding-based ChromaDB setup. Documents are embedded using the `all-MiniLM-L6-v2` model from Sentence Transformers. The top 3 semantically similar documents are retrieved using cosine similarity (see `retriever.py`).

- LLM Answer Generation
The GPT-4o model from OpenAI is used to generate responses grounded in retrieved context. Prompts are structured to enforce contextual grounding (see `llm_agent.py`).

- Hallucination Mitigation
To minimize hallucination, prompts explicitly instruct the model to "only use the following context" and "not make up any facts". While this is a simple form of mitigation, it was sufficient for the scope of this demo.

- Bonus 
    - Redis-based caching (see `redis_cache.py`)
    - Token-by-token streaming output (`stream=True` in `llm_agent.py`)
    - Logging of queries and responses to SQLite (`query_log.db` by `db_logger.py`)

## 🗂️ Project Structure
```
.
 ┣ data
 ┃ ┣ mock_data
 ┃ ┣ meta_data.json
 ┣ vector_store
 ┣ db_logger.py
 ┣ llm_agent.py
 ┣ main.py
 ┣ retriever.py
 ┣ example_query_response.json
 ┣ redis_cache.py
 ┣ requirements.txt
 ┗ README.md
```
- **data/mock_data**: Contains sample document data used for testing the system. The mock_data folder contains a total of 10 sample documents. These documents are a mix of real-world data collected from publicly available internet sources and carefully crafted mock data created for testing purposes. To effectively test the system’s retrieval accuracy and relevance, the documents cover a variety of topics related to dog health and nutrition, including recipes for dogs with cancer, general dog treat recipes, nutritional research, and unrelated animal welfare topics.    
- **data/meta_data.json**: Manages metadata for each document including id, title, topic, and source(article: from internet / mock: mock) in JSON format. 
- **vector_store**: Stores embedding vectors of documents.
- **db_logger.py**: Handles logging of each query, generated answer, and document sources to a local SQLite database (query_logs.db). This allows for auditing, debugging, or analyzing query history.
- **llm_agent.py**: Contains code for calling the OpenAI API(Model: GPT-4o), generating answers based on retrieved documents, and caching results with Redis. It includes support for streaming (stream=True) to return token-by-token responses 
- **main.py**: The main FastAPI application that hosts the API endpoint and handles client requests.  
- **retriever.py**: Responsible for generating embeddings and retrieving semantically similar documents. This module implements document retrieval using Chroma, a local embedding-based vector database. It embeds documents with Sentence Transformers (all-MiniLM-L6-v2) and retrieves the top-k most semantically similar documents for a given query.
- **example_query_response.json**: Stores sample test queries and their corresponding API responses for reference. 
- **redis_cache.py**: Contains Redis caching functions to save and retrieve cached answers by query.  
- **requirements.txt**: Lists required Python packages so users can install dependencies easily using `pip install -r requirements.txt`.  
- **README.md**: Provides an overall project explanation and instructions for setup and usage.



## 🚀 How to Run
### 1. Clone & Setup Environment
```bash
git clone https://github.com/connie-n/dog-cancer-diet-rag.git
cd dog-cancer-diet-rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**Note**: For security, this project does not include any API key. Please use your own key from your organization or personal OpenAI account.
Create a `.env` file in the root directory

```python
OPENAI_API_KEY="your-openai-api-key"
```

### 2. Prepare Data (if needed)
If not using mock data, place own data under mock_data folder. 
If want to use pdf file as data, place pdf files under data/docs_pdf folders and convert PDFs to text using doc_extract_txt.py
```bash
python doc_extract_txt.py
```

### 3. Generate Embeddings & Store
```bash
python retriever.py
```

### 4. Start the FastAPI Server
```bash
uvicorn main:app --reload
```

### 5. Redis Setup
Make sure you have Redis running locally before using the caching feature.  
To start Redis locally (on macOS/Linux):
```bash
redis-server
```

## 🧪 Example Query
POST request to /query:
```json
{
  "query": "What nutrients are beneficial for dogs with cancer?"
}
```

Sample response:
```json
{
  "answer": "Omega-3 fatty acids (EPA and DHA), antioxidants (Vitamin E, Vitamin C, Selenium), high-quality protein, glutamine, and low glycemic index carbohydrates are beneficial for dogs with cancer. These nutrients support immune function, reduce inflammation, and help maintain energy and muscle mass.",
  "sources": [
    "doc_4.txt",
    "doc_1.txt",
    "doc_2.txt"
    ]
}
```