import os

from dotenv import load_dotenv
from openai import OpenAI

from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma
from huggingface_hub import InferenceClient

load_dotenv()

# ===========================
# API KEYS
# ===========================

HF_API_KEY = os.getenv("HF_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ===========================
# HuggingFace Embedding Model
# ===========================

MODEL = "sentence-transformers/all-MiniLM-L6-v2"

hf_client = InferenceClient(
    api_key=HF_API_KEY
)


class HuggingFaceAPIEmbeddings(Embeddings):

    def embed_documents(self, texts):

        embeddings = []

        for text in texts:
            embedding = hf_client.feature_extraction(
                text,
                model=MODEL
            )
            embeddings.append(embedding)

        return embeddings

    def embed_query(self, text):

        return hf_client.feature_extraction(
            text,
            model=MODEL
        )


# ===========================
# Load ChromaDB
# ===========================

embedding_model = HuggingFaceAPIEmbeddings()

db = Chroma(
    persist_directory="./vector_db",
    embedding_function=embedding_model
)

# ===========================
# OpenRouter
# ===========================

llm = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


def ask(question):

    print("\nGenerating embedding...")

    query_embedding = embedding_model.embed_query(question)

    print(f"Embedding Dimension : {len(query_embedding)}")

    print("\nSearching ChromaDB...\n")

    results = db.similarity_search_with_score(
        question,
        k=3
    )

    context = ""

    for i, (doc, score) in enumerate(results):

        print("=" * 80)
        print(f"Chunk {i+1}")
        print(f"Similarity Score : {score}")
        print()
        print(doc.page_content)
        print()

        context += doc.page_content + "\n\n"

    prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not available in the context simply reply

"I don't know."

Context:

{context}

Question:

{question}
"""

    response = llm.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You answer only from the provided context."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\n")
    print("=" * 80)
    print("FINAL ANSWER")
    print("=" * 80)
    print()

    print(response.choices[0].message.content)


# ===========================
# Chat Loop
# ===========================

while True:

    question = input("\nAsk Question (type exit to quit): ")

    if question.lower() == "exit":
        break

    ask(question)