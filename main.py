from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever 

MODEL_NAME = "llama3.2"

app = Flask(__name__)
CORS(app)

model = OllamaLLM(model=MODEL_NAME)

template = """
You are an expert agricultural assistant.
You must give the answer in a clear, well-structured format.

Guidelines:
- Start with a **Recommended Crop** line if possible.
- Provide reasons in bullet points.
- Include any environmental requirement matches (nitrogen, potassium, phosphorus, temperature, humidity, soil pH, etc.).
- Keep sentences short and easy to read.
- If the crop cannot be determined, politely say so.

Relevant data:
{reviews}

Question:
{question}

Now provide your answer in the following format:
Recommended Crop: <crop name or "Not sure">
Reasons:
- ...
- ...
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    if question in ["hi", "hello", "hey"]:
     return jsonify({"answer": "Hello, how can I help you?"})

    reviews = retriever.invoke(question)
    result = chain.invoke({"reviews": reviews, "question": question})
    return jsonify({"answer": result})

if __name__ == "__main__":
    print("[INFO] Backend running at http://127.0.0.1:5000")
    app.run(debug=True)
