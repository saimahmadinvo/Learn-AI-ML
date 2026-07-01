from langchain_community.document_loaders import PyPDFLoader

def loader(): 
    loader = PyPDFLoader(
    file_path="./saim.pdf",
    mode="page"
    )

    # Read the PDF
    documents = loader.load()

    return documents

print(loader())
