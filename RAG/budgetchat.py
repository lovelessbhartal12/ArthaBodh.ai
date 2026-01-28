import re
from pprint import pprint
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document



PDF_PATH = "Webside Final budget Speech 2_15_qbn3jyt.pdf"


NUMBER_PATTERN = r"[0-9०-९]+"



loader = PyMuPDFLoader(PDF_PATH)
documents = loader.load()



def is_data_heavy(text: str) -> bool:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    numeric_lines = sum(
        1 for line in lines if len(re.findall(NUMBER_PATTERN, line)) >= 2
    )
    return numeric_lines >= 2



def extract_stat_facts(text: str):
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



def parse_table(text: str):
    rows = []
    for line in text.split("\n"):
        if len(re.findall(NUMBER_PATTERN, line)) >= 3:
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) >= 3:
                rows.append(parts)
    return rows


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



fact_chunks = []

for doc in documents:
    facts = extract_stat_facts(doc.page_content)
    for fact in facts:
        fact_chunks.append(
            Document(
                page_content=fact,
                metadata={
                    "type": "stat_fact",
                    "source": "budget_speech"
                }
            )
        )



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



final_documents = text_chunks + fact_chunks + table_chunks



print("Narrative chunks :", len(text_chunks))
print("Statistical facts:", len(fact_chunks))
print("Table sentences  :", len(table_chunks))
print("TOTAL documents  :", len(final_documents))

print("\nSample output:\n")
pprint(final_documents[10].page_content)