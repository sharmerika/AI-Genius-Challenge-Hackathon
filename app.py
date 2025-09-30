from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Azure Search setup
SEARCH_ENDPOINT = "https://indexsearch92.search.windows.net" #okay to post they were deleted
SEARCH_API_KEY = "Azure_key" #okay to post they were deleted
SEARCH_INDEX = "indexsearch92"

# OpenAI setup
OPENAI_ENDPOINT = "https://nwopnai92.openai.azure.com/" #okay to post they were deleted
OPENAI_API_KEY = "Azure_key"
EMBEDDING_DEPLOYMENT = "text-embedding-ada-002"
COMPLETION_DEPLOYMENT = "gpt-4"

@app.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q")
    if not question:
        return jsonify({"error": "Missing question"}), 400

    
    embedding_response = requests.post(
        f"{OPENAI_ENDPOINT}/openai/deployments/{EMBEDDING_DEPLOYMENT}/embeddings?api-version=2023-05-15",
        headers={"api-key": OPENAI_API_KEY},
        json={"input": question}
    )
    embedding_data = embedding_response.json()
    if "data" not in embedding_data or not embedding_data["data"]:
        return jsonify({"error": "Embedding failed", "details": embedding_data}), 500

    embedding = embedding_data["data"][0]["embedding"]

    
    search_response = requests.post(
        f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/search?api-version=2023-11-01",
        headers={"api-key": SEARCH_API_KEY, "Content-Type": "application/json"},
        json={
            "vector": {
                "value": embedding,
                "fields": "contentVector",
                "k": 5
            },
            "select": "content"
        }
    )

    search_json = search_response.json()
    if "value" not in search_json:
        return jsonify({
            "question": question,
            "error": "Search failed",
            "details": search_json
        }), 500

    retrieved_docs = [doc["content"] for doc in search_json["value"]]

    
    prompt = f"""
You are a forensic analyst. Based on the following documents, answer the question clearly and accurately.

Documents:
{retrieved_docs}

Question:
{question}

Answer:
"""

    
    completion_response = requests.post(
        f"{OPENAI_ENDPOINT}/openai/deployments/{COMPLETION_DEPLOYMENT}/chat/completions?api-version=2023-05-15",
        headers={"api-key": OPENAI_API_KEY, "Content-Type": "application/json"},
        json={
            "messages": [
                {"role": "system", "content": "You are a forensic analyst helping identify the root cause of a cybersecurity incident."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "max_tokens": 500
        }
    )

    completion_data = completion_response.json()
    if "choices" not in completion_data or not completion_data["choices"]:
        return jsonify({"error": "Completion failed", "details": completion_data}), 500

    answer = completion_data["choices"][0]["message"]["content"]

    return jsonify({
        "question": question,
        "answer": answer,
        "sources": retrieved_docs
    })
if __name__ == "__main__":
    app.run(debug=True)
