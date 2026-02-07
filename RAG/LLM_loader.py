# llm_loader.py
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import torch


def load_llm(
    model_path: str = "./qwen_nepali_budget_merged",
    temperature: float = 0.1,
    max_new_tokens: int = 512
):

    tokenizer = AutoTokenizer.from_pretrained(model_path)

    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    return llm

