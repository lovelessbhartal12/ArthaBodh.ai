import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

PDF_PATH = "nepal_constituiton.pdf"
NUMBER_PATTERN = r"[0-9०-९]+"  

def load_pdf(pdf_path=PDF_PATH):
    """
    Load PDF using PyMuPDFLoader and ensure UTF-8 encoding.
    """
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    
    # Ensure UTF-8 for all page content
    for doc in docs:
        if doc.page_content:
            doc.page_content = doc.page_content.encode('utf-8', errors='ignore').decode('utf-8')
    
    return docs

def is_data_heavy(text: str) -> bool:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    numeric_lines = sum(
        1 for line in lines if len(re.findall(NUMBER_PATTERN, line)) >= 2
    )
    return numeric_lines >= 2

def clean_narrative_documents(documents):
    text_sections = []
    for doc in documents:
        if not is_data_heavy(doc.page_content):
            text_sections.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    text_chunks = text_splitter.split_documents(text_sections)
    for chunk in text_chunks:
        chunk.metadata.update({
            "type": "narrative",
            "source": "budget_speech"
        })

    return text_chunks

def get_cleaned_documents(pdf_path=PDF_PATH):
    docs = load_pdf(pdf_path)
    return clean_narrative_documents(docs)