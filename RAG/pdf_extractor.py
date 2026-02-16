# pdf_extractor.py
import re
from langchain_core.documents import Document
from pdf_loader import get_cleaned_documents, load_pdf, NUMBER_PATTERN


def extract_stat_facts(text):
    facts = []
    keywords = [
        "प्रतिशत", "अबव", "करोड", "लाख", "हजार",
        "डलर", "मेगावाट", "वृद्धि", "पुगेको", "भएको"
    ]
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        if len(re.findall(NUMBER_PATTERN, line)) >= 1:
            if any(word in line for word in keywords):
                facts.append(line)
    return facts

def extract_stat_facts_from_documents(documents):
    fact_chunks = []
    for doc in documents:
        facts = extract_stat_facts(doc.page_content)
        for fact in facts:
            fact_chunks.append(
                Document(
                    page_content=fact,
                    metadata={"type": "stat_fact", "source": "budget_speech"}
                )
            )
    return fact_chunks



def parse_table(text):
    rows = []
    for line in text.split("\n"):
        if len(re.findall(NUMBER_PATTERN, line)) >= 3:
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) >= 3:
                rows.append(parts)
    return rows

def table_to_sentences(documents):
    table_chunks = []
    for doc in documents:
        rows = parse_table(doc.page_content)
        for row in rows:
            sector, expense_type, amount = row[:3]
            sentence = (
                f"In fiscal year 2081/82, the {expense_type.lower()} "
                f"budget allocated to the {sector} sector is NPR {amount}."
            )
            table_chunks.append(
                Document(
                    page_content=sentence,
                    metadata={
                        "sector": sector,
                        "expense_type": expense_type,
                        "type": "table",
                        "year": "2081/82"
                    }
                )
            )
    return table_chunks




def get_final_documents(pdf_path="nepal_constituiton.pdf"):
    narrative_docs = get_cleaned_documents(pdf_path)
    raw_docs = load_pdf(pdf_path)
    
    stat_facts = extract_stat_facts_from_documents(raw_docs)
    table_sentences = table_to_sentences(raw_docs)
    final_docs=narrative_docs + stat_facts + table_sentences

    return final_docs




# if __name__ == "__main__":
#     chunks = get_final_documents()
#     for i, doc in enumerate(chunks[:5], 1):
#         print(f"\n--- Chunk {i} ---")
#         print(doc.page_content[:800])
#         print("Metadata:", doc.metadata)

  