# budget_chatbot_deepseek.py

from LLM_loader import load_llm
from Embedding import build_and_save_vector_store
from prompts import budget_prompt
import re

def ask_budget_chatbot(query, k=5):
    """
    Ask the budget chatbot using DeepSeek V3.1 Cloud via Ollama.
    Returns plain Nepali answers.
    """
   
    llm = load_llm()

    
    vector_store = build_and_save_vector_store()

   
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    context_text = "\n".join([doc.page_content for doc in docs])

    
    prompt_template = budget_prompt()

   
    final_prompt = prompt_template.format(instruction=context_text, input=query)

 
    response = llm.generate([final_prompt])

    
    raw_answer = response.generations[0][0].text
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", raw_answer)

   
    text = re.sub(r"^\s*[\*\-]+\s*", "", text, flags=re.MULTILINE)

  
    text = re.sub(r"^\s*\d+\.\s*", "", text, flags=re.MULTILINE)

    text = text.replace("\n", " ")

    # 5. Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


