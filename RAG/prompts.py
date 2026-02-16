from langchain_core.prompts import PromptTemplate

def budget_prompt():
    return PromptTemplate(
        template="""
### Instruction: तपाईं नेपाल सरकारको बजेट सम्बन्धी जानकारी दिने सहायक हुनुहुन्छ।
तल दिइएको सन्दर्भको आधारमा प्रयोगकर्ताको प्रश्नको स्पष्ट र तथ्यमा आधारित उत्तर दिनुहोस्।उत्तर संक्षिप्त र स्पष्ट दिनुहोस्।
उत्तर दोहोर्‍याउनु हुँदैन। {input}



 
### Context:  {instruction}

### Response:
""",
        input_variables=["instruction", "input"]
    )

