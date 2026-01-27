import re
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

PDF_PATH = "Webside Final budget Speech 2_15_qbn3jyt.pdf"
NUMBER_PATTERN = r"[0-9०-९]+"  

def load_pdf(pdf_path=PDF_PATH):
    loader = PyMuPDFLoader(pdf_path)
    return loader.load()

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
        chunk_overlap=100
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

# # Optional sanity check
# if __name__ == "__main__":
#     cleaned_docs = get_cleaned_documents()
#     print(f"Cleaned narrative chunks: {len(cleaned_docs)}")
#     from pprint import pprint
#     pprint(cleaned_docs[:2])
