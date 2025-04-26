import PyPDF2
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(paths):
    documents = []
    for path in paths:
        try:
            if path.lower().endswith('.pdf'):
                with open(path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = "".join(page.extract_text() for page in reader.pages)
                    documents.append(Document(page_content=text, metadata={"source": path}))
            else:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    documents.append(Document(page_content=content, metadata={"source": path}))
        except Exception as e:
            print(f"Error loading {path}: {e}")
    return documents

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    return splitter.split_documents(documents)