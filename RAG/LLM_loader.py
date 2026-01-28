# llm_loader.py
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm(
    model_name: str = "deepseek-v3.1:671b-cloud",
    temperature: float = 0.3,
    max_output_tokens: int = 512
):
    """
    Load DeepSeek V3.1 (Cloud) via Ollama
    """
    llm = OllamaLLM(
        model=model_name,
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )
    return llm
