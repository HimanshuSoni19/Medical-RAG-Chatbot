# 🏥 Medical RAG Chatbot

An intelligent, Retrieval-Augmented Generation (RAG) powered chatbot designed to provide context-aware medical information using private document knowledge.

---

## 🚀 Overview
This project implement a full-stack RAG pipeline that allows users to chat with their medical PDF documents. It uses **LLama-3** (via Groq) for lightning-fast inference and **FAISS** for efficient vector similarity search.

![Medical RAG Workflow](Medical+RAG+Workflow.png)

## ✨ Key Features
- **PDF Intelligence**: Automatically ingests and processes medical documents from the `data/` directory.
- **Fast Inference**: Powered by **Groq** for near-instant responses.
- **Context-Aware**: High-precision retrieval using **HuggingFace MiniLM** embeddings.
- **User Interface**: Clean and responsive web interface built with **Flask** and **Vanilla CSS**.
- **Session Memory**: Remembers your conversation within the chat session.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Generative AI Framework** | [LangChain](https://www.langchain.com/) |
| **LLM Inference** | [Groq (Llama-3.3-70b)](https://groq.com/) |
| **Embeddings** | [HuggingFace (all-MiniLM-L6-v2)](https://huggingface.co/) |
| **Vector Store** | [FAISS](https://github.com/facebookresearch/faiss) |
| **Backend** | [Flask](https://flask.palletsprojects.com/) |
| **Frontend** | HTML5, Modern CSS3 |

## ⚙️ Quick Start

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone <your-repo-url>
cd "Rag Medical Chatbot"
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```

### 3. Load Your Data
Place your medical PDFs in the `data/` folder, then run the ingestion script:
```bash
python app/components/data_loader.py
```

### 4. Run the App
```bash
python app/application.py
```
Visit `http://127.0.0.1:5000` in your browser.

## 📁 Project Structure
```text
├── app/
│   ├── components/      # Core RAG logic (PDF loading, embeddings, LLM)
│   ├── static/          # CSS and Assets
│   ├── templates/       # HTML UI
│   └── application.py   # Flask App Entry
├── data/                # Your PDF documents
├── vectorstore/         # FAISS index (local memory)
├── .env                 # API Keys (gitignored)
└── .gitignore           # File exclusions
```

## 🗺️ Roadmap
- [ ] **Dockerization**: Containerize for easy deployment.
- [ ] **Security Scanning**: Integrate Aqua Trivy for image security.
- [ ] **CI/CD**: Auto-deployment via Jenkins to AWS Runner.
- [ ] **Multi-source Data**: Support for web scraping and text files.

---
*Disclaimer: This tool is for informational purposes only and should not replace professional medical advice.*