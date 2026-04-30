import os
import pandas as pd
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

EMBED_MODEL = "mxbai-embed-large"
DB_DIR = "./chroma_agri_db"
CSV_FILE = "Agriculture.csv"

embeddings = OllamaEmbeddings(model=EMBED_MODEL)

add_documents = not os.path.exists(DB_DIR)

vector_store = Chroma(
    collection_name="agriculture",
    persist_directory=DB_DIR,
    embedding_function=embeddings
)

if add_documents:
    print("[INFO] Creating vector database...")
    df = pd.read_csv(CSV_FILE)
    documents = []
    ids = []
    for i, row in df.iterrows():
        content = "Title: " + str(row.get("Title", "")) + " | Review: " + str(row.get("Review", ""))
        documents.append(Document(
            page_content=content,
            metadata={"rating": row.get("Rating", ""), "date": row.get("Date", "")}
        ))
        ids.append(str(i))
    vector_store.add_documents(documents=documents, ids=ids)
    print("[INFO] Vector DB created.")

retriever = vector_store.as_retriever(search_kwargs={"k": 5})
