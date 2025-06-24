# dog-cancer-diet-rag



## 🗂️ Project Structure
\```
.
 ┣ data
 ┃ ┣ mock_data
 ┣ 📄main.py
 ┣ vector_store
 ┣ llm_agent.py
 ┣ retriever.py
 ┣ example_query_response.json
 ┣ requirements.txt
 ┗ README.md
\```


## 🚀 How to Run
### 1. Clone & Setup Environment
```bash
git clone https://github.com/connie-n/dog-cancer-diet-rag.git
cd dog-cancer-diet-rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**NOte**: For security, this project does not include any API key. Please use your own key from your organization or personal OpenAI account.
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