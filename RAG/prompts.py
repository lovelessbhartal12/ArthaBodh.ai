from langchain_core.prompts import PromptTemplate

def budget_prompt():
    return PromptTemplate(
        template="""
तपाईंले तलका कागजातहरू पढ्नुभयो:
{context}

प्रश्न: {question}

नेपाली भाषामा छोटकरीमा स्पष्ट जवाफ दिनुहोस्।
""",
        input_variables=["context", "question"]
    )
