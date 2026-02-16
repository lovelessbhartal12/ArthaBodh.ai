from langchain_core.prompts import PromptTemplate

def budget_prompt():
    return PromptTemplate(
        template="""
Instruction: माथिको विवरण अनुसार
 {input}
Input: {instruction}

Response:
""",
        input_variables=["instruction", "input"]
    )

