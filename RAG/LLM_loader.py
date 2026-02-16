# llm_loader.py
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline


def load_llm(
    temperature: float = 0.1,
    max_new_tokens: int = 512
):
    # -----------------------
    # Resolve absolute path
    # -----------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "qwen_nepali_budget_merged")

    # -----------------------
    # Load tokenizer (LOCAL ONLY)
    # -----------------------
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True,
        local_files_only=True
    )

    # -----------------------
    # Load model (LOCAL ONLY)
    # -----------------------
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        trust_remote_code=True,
        local_files_only=True
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # -----------------------
    # HF pipeline
    # -----------------------
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        return_full_text=False
    )

    # -----------------------
    # LangChain wrapper
    # -----------------------
    llm = HuggingFacePipeline(pipeline=pipe)

    return llm
