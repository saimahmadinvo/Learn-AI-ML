import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from splitter import splitter
from langchain_core.embeddings import Embeddings
from langchain_chroma import Chroma

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

MODEL = "sentence-transformers/all-MiniLM-L6-v2"

client = InferenceClient(
    api_key=HF_API_KEY,
)


class HuggingFaceEmbeddingsAPI(Embeddings):

    def embed_documents(self, texts):
        embeddings = []

        for text in texts:
            embedding = client.feature_extraction(
                text,
                model=MODEL,
            )
            embeddings.append(embedding)

        return embeddings

    def embed_query(self, text):
        return client.feature_extraction(
            text,
            model=MODEL,
        )


def create_vector_db():

    chunks = splitter()

    embedding_model = HuggingFaceEmbeddingsAPI()

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./vector_db"
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")

    return db


if __name__ == "__main__":
    create_vector_db()