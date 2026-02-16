# faiss_builder.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from pdf_extractor import get_final_documents
save_path = "faiss_budget_index1"
def build_and_save_vector_store(pdf_path=None, save_path="faiss_budget_index1"):

    documents = get_final_documents() if pdf_path is None else get_final_documents(pdf_path)
    
    
    embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base",
    encode_kwargs={"normalize_embeddings": True}
)
    
    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model
    )
    
    
    vector_store.save_local(save_path)
    
    # print(f"Vector store saved to '{save_path}' with {len(documents)} documents")
    return vector_store

if __name__ == "__main__":
    build_and_save_vector_store()
