import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

BASE_MODEL = "Qwen/Qwen3-1.7B"
LORA_PATH = "./qwen_nepali_budget_lora"
MERGED_MODEL_PATH = "../RAG/qwen_nepali_budget_merged"

# -----------------------
# Load tokenizer


def save():
    #load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(LORA_PATH, trust_remote_code=True)

    # Load base model
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        device_map="auto",
        torch_dtype=torch.float16,
        trust_remote_code=True
    )

   
    # Load LoRA adapters

    model = PeftModel.from_pretrained(model, LORA_PATH)
    model = model.merge_and_unload()
    model.save_pretrained(MERGED_MODEL_PATH)
    tokenizer.save_pretrained(MERGED_MODEL_PATH)



if __name__ == "__main__":
    save()


