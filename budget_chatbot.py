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
    # 1. Load the DeepSeek cloud LLM
    llm = load_llm(model_name="deepseek-v3.1:671b-cloud", temperature=0.3, max_output_tokens=512)

    # 2. Build or load your vector store (RAG)
    vector_store = build_and_save_vector_store()

    # 3. Create a retriever and get top-k documents
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    # 4. Combine document contents
    context_text = "\n".join([doc.page_content for doc in docs])

    # 5. Get the prompt template
    prompt_template = budget_prompt()

    # 6. Format the final prompt (force Nepali output)
    final_prompt = prompt_template.format(context=context_text, question=query)
    final_prompt = f"तपाईं नेपाली भाषामा मात्र उत्तर दिनुहोस्।\n\n{final_prompt}"

    # 7. Generate response using DeepSeek Cloud
    response = llm.generate([final_prompt])

    # 8. Extract the generated text
    raw_answer = response.generations[0][0].text
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", raw_answer)

    # 2. Remove bullet symbols at start of line (if any)
    text = re.sub(r"^\s*[\*\-]+\s*", "", text, flags=re.MULTILINE)

    # 3. Remove numbering like 1., 2., 3. at start of lines
    text = re.sub(r"^\s*\d+\.\s*", "", text, flags=re.MULTILINE)

    # 4. Replace newlines with space
    text = text.replace("\n", " ")

    # 5. Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

   





    # return answer


# if __name__ == "__main__":
#     query = "प्रदेश ३ का विद्यालयहरूका लागि 2082/2083 को बजेटमा कस्तो व्यवस्था गरिएको छ? कृपया मात्र तथ्याङ्क र योजनामा आधारित जवाफ दिनुहोस्, बुलेट वा नम्बर बिना।"

#     answer = ask_budget_chatbot(query)
#     print("ANSWER:\n", answer)
