# ArthaBodh – Nepali Budget Intelligence System

An end-to-end Nepali Budget Question-Answering system that combines LoRA fine-tuned multilingual LLM + Retrieval-Augmented Generation (RAG) to deliver accurate, context-aware responses about Nepal’s national budget.

The system is designed to understand instruction-based Nepali queries, retrieve relevant sections from official budget documents, and generate grounded, concise answers.

## 🚀 Features

- Ask questions about Nepal’s national budget in Nepali

- Instruction-based Q&A format (Instruction + Context + Response)

- Fine-tuned multilingual LLM for domain-specific understanding

- RAG pipeline to reduce hallucination

- Context-grounded answers

- Streamlit interactive UI

- Deployable via Hugging Face or local inference

---

## 🧠 Tech Stack (with Purpose)

- **Qwen3-1.7B (Fine-tuned with LoRA)**

  Purpose: Acts as the core LLM for generating final answers in Nepali.

  Detail: It processes the retrieved chunks from the legal documents alongside the user query to provide contextually accurate responses.

- **Multilingual E5 Base**
  Purpose: Used to generate dense vector embeddings for Nepali text.

  Detail: This model transforms text chunks from the Nepal Sambidhan into mathematical vectors that capture semantic meaning, facilitating accurate retrieval.

- **PEFT (LoRA)**

  Purpose: Used for Parameter-Efficient Fine-Tuning of the Qwen model.

  Detail: By targeting the query and value projections, LoRA allows the model to adapt to the specific nuances of the Nepal Budget dataset without the high computational cost of full-parameter training.

- **FAISS (Facebook AI Similarity Search)**

  Purpose: Serves as the high-performance vector database.

  Detail: It stores the embeddings of the split text and enables rapid "Retrieve Engine" functionality using Cosine Similarity to find the most relevant legal/budgetary context.

- **Text Splitting (Recursive/Character)**

  Purpose: Pre-processes the Nepal Sambidhan into manageable segments.

  Detail: Ensures that the input to the embedding model stays within token limits while preserving the structural integrity of the legal articles.

- **Python**

  Purpose: The primary programming language for the entire pipeline.

  Detail: Orchestrates the flow between the retrieval system (RAG) and the fine-tuned generation model.

- **Instruction Preparation & Evaluation**

  Purpose: Ensures the quality of the fine-tuning process.

  Detail: Converts the Nepal Budget dataset into instruction-response pairs and monitors performance via training loss (0.2874) and validation loss (0.3028).

---

## 🏗️ System Architecture & Workflow

### 🔄 Overall Workflow Diagram

![Workflow Diagram](assets/workflow.png)

### Workflow Explanation

1. User asks a budget-related question in Nepali

2. Question is embedded using multilingual embedding model

3. FAISS retrieves relevant budget document chunks

4. Context + Instruction formatted prompt is created

5. Fine-tuned Qwen model generates answer

6. Answer displayed in Streamlit UI

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/lovelessbhartal12/ArthaBodh.ai
cd ArthaBodh.ai
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```
pip install -r requirement.txt
```

### 4. Save Finetuned Model

```
cd Finetune
python save_model_to_use.py
```

### 5. Start UI

```
cd RAG
streamlit run app.py
```

## 🎯 Why RAG + Fine-Tuning?

- Fine-tuning improves domain understanding

- RAG ensures factual grounding

- Together → Reduced hallucination + Accurate contextual answers

## ⚠️ Limitations

- Model performance depends on dataset quality

- Limited training samples may reduce generalization

- Requires proper chunking for best RAG performance

- Large documents may increase latency

## 👤 Author

<table> <tr><td align="center"> <a href="https://github.com/lovelessbhartal12"> <img src="https://avatars.githubusercontent.com/u/103515260?v=4" width="100px;" alt="Contributor 2"/> <br /> <sub><b>Loblesh Bhartal(RAG)</b></sub> </a> </td>   <td align="center"> <a href="https://github.com/roshan-acharya"> <img src="https://avatars.githubusercontent.com/u/85246971?v=4" width="100px;" alt="Roshan Acharya"/> <br /> <sub><b>Roshan Acharya(Finetune)</b></sub> </a> </td> </table>
