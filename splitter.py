from langchain_text_splitters import RecursiveCharacterTextSplitter
from loader import loader

def splitter(): 

    documents = loader()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    chunks = splitter.split_documents(documents)

    return chunks
