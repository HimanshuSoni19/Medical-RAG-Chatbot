# 🏥 The Story of the Medical RAG Chatbot

Welcome to the journey of building a **Retrieval-Augmented Generation (RAG)** application. This documentation isn't just a list of files; it's a story of how a chatbot "thinks" and "remembers."

By understanding this story, you'll be able to build 50% of any RAG application yourself next time. Let's begin!

---

## 🏗️ Chapter 1: The Foundation (Data Ingestion)

Imagine you have a library of medical books (PDFs). You want a chatbot that doesn't just guess answers but looks them up in these specific books. To do this, we need to prepare the "brain" of our chatbot.

### 1. The Gatherer: `pdf_loader.py`
**Why we needed it:** A computer can't "read" a 500-page PDF all at once. It would get overwhelmed. We need to break the books into small, digestible "pages."
- **What it does:** It scans your `data/` folder, picks up every PDF, and breaks them into small chunks (e.g., 500 characters each).
- **How it works:** It uses `PyPDFLoader` to read the text and `RecursiveCharacterTextSplitter` to cut it into pieces that overlap slightly (so no sentences are cut in half).
- **The Benefit:** Small chunks make searching much faster and more accurate.

### 2. The Translator: `embeddings.py`
**Why we needed it:** Computers don't understand words like "heartburn" or "diagnosis"—they only understand numbers. We need a way to translate medical text into a math-based "coordinate system."
- **What it does:** It takes a chunk of text and turns it into a long list of numbers called a **Vector**.
- **How it works:** It uses a `HuggingFaceEmbeddings` model (`all-MiniLM-L6-v2`). This model is like a dictionary that maps words to their meanings in a multi-dimensional space.
- **The Benefit:** Now, the computer can find "similarity" by measuring the "distance" between two lists of numbers.

### 3. The Librarian: `vector_store.py`
**Why we needed it:** If you have 50,000 text chunks, searching through them one by one every time someone asks a question would be too slow. We need a high-speed library filing system.
- **What it does:** It takes all those translated numbers (vectors) and organizes them into a **FAISS** database.
- **How it works:** It saves the organized index to the `vectorstore/` folder. When a question comes in, it doesn't "read"—it "scans" the coordinates to find the closest match in milliseconds.
- **The Benefit:** Instant retrieval of the most relevant information from thousands of pages.

---

## 💬 Chapter 2: The Conversation (The Chat Pipeline)

Now that our library is ready, how does a user actually talk to it?

### 4. The Brain: `llm.py`
**Why we needed it:** Finding the right text isn't enough. We need someone who can *speak* human languages, summarize facts, and follow instructions.
- **What it does:** It connects to a powerful AI model (Llama-3 via Groq) that is trained to hold conversations.
- **How it works:** It uses an API key to send the text to a "supercomputer" (Groq) that processes language at lightning speed.
- **The Benefit:** The chatbot sounds human and can explain complex medical terms simply.

### 5. The Researcher: `retriever.py`
**Why we needed it:** This is the "glue." It's the bridge between the **Librarian** (who has the data) and the **Brain** (who can speak).
- **What it does:** It creates a **RetrievalQA** chain. 
- **The Story:** When you ask "What are the symptoms of Flu?", this component:
    1. Translates your question into numbers.
    2. Asks the **Librarian** for the most relevant medical text.
    3. Combines that text with your question into a "Prompt" (e.g., *"Using this text: [Relevant Text], answer the question: [Your Question]"*).
    4. Sends that prompt to the **Brain**.
- **Implementation Detail:** We use a `PromptTemplate` to tell the AI exactly how to behave (e.g., "Answer in 2-3 lines").

### 6. The Host: `application.py`
**Why we needed it:** We need a place for the user to type and see the results—a web page.
- **What it does:** It's a Flask server that manages the "Session" (remembering previous messages) and renders the HTML templates.
- **How it works:** It listens for your question, calls the **Researcher**, and sends the answer back to your screen.
- **Benefit:** It makes the complex RAG technology feel like a simple, friendly chat app.

---

## 🛠️ Chapter 3: The Support Cast (Infrastructure)

Every great story needs a supporting cast to keep things moving.

- **`config.py` (The Map):** Stores paths and API keys so you don't have to hunt for them in every file.
- **`logger.py` & `custom_exception.py` (The Witnesses):** They watch everything. If something fails (like a missing API key), they tell you exactly which file and which line broke so you can fix it quickly.

---

## 🚀 Stuff You Need to Know (The Secret Sauce)

If you want to build your own RAG app, remember these three rules:
1. **Garbage In, Garbage Out:** If your PDFs are blurry or have bad text, your chatbot will give bad answers.
2. **The "k" Factor:** In `retriever.py`, we set `k=1`. This means we only give the AI *one* chunk of information. If the answer is complex, you might need `k=3` or `k=5` to give it more context.
3. **Chunk Size Matters:** If chunks are too small (100 characters), they lose meaning. If they are too big (5000 characters), they confuse the AI. 500-1000 is usually the "sweet spot."

---

## 🎨 How to Use This Documentation

1.  **To add new books:** Drop PDFs in `data/` and run `python app/components/data_loader.py`. This triggers Chapter 1.
2.  **To change the AI's personality:** Edit the `CUSTOM_PROMPT_TEMPLATE` in `retriever.py`.
3.  **To start the server:** Run `python app/application.py` and open your browser!

*You are now equipped with the knowledge of how pieces fit together. Go build something amazing!*

---

# 🩺 Ultra-Deep Dive: Every Line Explained

Welcome! This is a complete breakdown of every Python file in your project. We will go through them one by one, explaining what every block of code does in plain English.

---

## ⚙️ 1. `app/config/config.py`
**Purpose:** This is the "Settings" page. Instead of typing folder names or API keys in every file, we put them here once.

| Code Block | What it does (Line-by-Line) |
| :--- | :--- |
| `import os` | Brings in the `os` tool so Python can talk to your Windows folders. |
| `from dotenv import load_dotenv` | Brings in a tool to read your `.env` file (where your secret keys are). |
| `load_dotenv()` | Actually runs the tool. Now Python "knows" what's inside your `.env` file. |
| `HF_TOKEN = os.environ.get(...)` | Looks inside `.env` for something named `HF_TOKEN` and saves it here. |
| `DB_FAISS_PATH = "vectorstore/db_faiss"` | Tells the app exactly where to save its "memory" folder. |
| `CHUNK_SIZE = 500` | Defines how big each "snippet" of medical text should be. |

---

## 🛡️ 2. `app/common/custom_exception.py`
**Purpose:** This handles errors. If the app breaks, this file "takes a photo" of the error and tells you where it happened.

| Code Block | What it does |
| :--- | :--- |
| `class CustomException(Exception):` | We are creating our own "Type" of error. It's like a custom warning light. |
| `sys.exc_info()` | This is the "Detective" tool. It asks Python: *"Hey, who just broke? What line were they on?"* |
| `exc_tb.tb_lineno` | Specifically grabs the **Line Number** where the code crashed. |
| `return f"{message} | Error: {error_detail}..."` | Creates a neat, readable sentence that tells you exactly why and where things went wrong. |

---

## 📄 3. `app/components/pdf_loader.py`
**Purpose:** This file reads your PDFs and chops them up.

| Code Block | What it does |
| :--- | :--- |
| `DirectoryLoader(..., glob="*.pdf")` | Tells the computer: *"Look inside the data folder, but ONLY pick up files that end in .pdf"* |
| `loader.load()` | This is the "Reading" action. It opens every PDF and extracts all the text into a list. |
| `RecursiveCharacterTextSplitter` | Think of this as a pair of scissors. It doesn't just cut anywhere; it tries to find the end of a paragraph so it doesn't cut a sentence in half. |
| `split_documents(documents)` | Runs the scissors on the text we just read. Now we have thousands of tiny "text chunks." |

---

## 🔢 4. `app/components/embeddings.py`
**Purpose:** This turns words into math.

| Code Block | What it does |
| :--- | :--- |
| `HuggingFaceEmbeddings(model_name=...)` | We load a pre-trained "Dictionary" from HuggingFace. This dictionary doesn't define words; it gives them "Coordinates." |
| **Example:** | The model knows that "Sore Throat" is mathematically closer to "Cough" than it is to "Banana." |

---

## 🏛️ 5. `app/components/vector_store.py`
**Purpose:** This is the "Hard Drive" for the chatbot's memory.

| Code Block | What it does |
| :--- | :--- |
| `FAISS.from_documents(...)` | This takes all those text chunks and their "Coordinates" and organizes them into a super-fast searchable index called **FAISS**. |
| `db.save_local(DB_FAISS_PATH)` | Actually saves that index to your computer so you don't have to recalculate it every time. |
| `FAISS.load_local(...)` | Reads that saved memory back so the chatbot can "remember" it. |

---

## 🏭 6. `app/components/data_loader.py`
**Purpose:** The "Factory Manager." It runs all the steps above in order.

| Code Block | What it does |
| :--- | :--- |
| `if __name__ == "__main__":` | This means: *"Only run this code if I double-click this specific file."* |
| `process_and_store_pdfs()` | It calls: 1. Read PDF -> 2. Split into Chunks -> 3. Save to Vector Store. |

---

## 🤖 7. `app/components/llm.py`
**Purpose:** Connecting to the AI "Voice" (Groq).

| Code Block | What it does |
| :--- | :--- |
| `ChatGroq(...)` | We connect to Groq's supercomputers. We tell it: <br>1. **Model:** Use `llama-3.3-70b` (very smart). <br>2. **Temperature:** 0.3 (Stay scientific, don't be too creative/funny). <br>3. **Max Tokens:** 1024 (Keep the answer reasonably short). |

---

## 🔍 8. `app/components/retriever.py`
**Purpose:** The "Librarian." Finding the right page for the user's question.

| Code Block | What it does |
| :--- | :--- |
| `CUSTOM_PROMPT_TEMPLATE` | This is the instruction manual for the AI. We tell it: *"Use this medical text to answer, and if you don't know the answer, just say you don't know."* |
| `db.as_retriever(search_kwargs={'k': 1})` | This turns our memory (FAISS) into a search engine. `k: 1` means: *"Find the SINGLE best paragraph that answers this question."* |
| `RetrievalQA.from_chain_type(...)` | This is the "Glue." it binds the **Searcher** and the **AI Speaker** together. |

---

## 💻 9. `app/application.py`
**Purpose:** The "Face" of the app. This is what you see in the browser.

| Code Block | What it does |
| :--- | :--- |
| `@app.route("/")` | Tells the server: *"When someone visits my website's main page, run the code below."* |
| `if "messages" not in session:` | If this is a new visitor, create an empty list to store their chat history. |
| `request.form.get("prompt")` | This grabs whatever text the user typed into the chat box. |
| `qa_chain.invoke(...)` | Sends the user's question into our RAG system to get the answer. |
| `return render_template("index.html", ...)` | Takes the answer and puts it inside the HTML code so it shows up on your screen. |

---

### **Summary of the "Chain of Events"**
1. **User types:** "What is Cancer?"
2. **`application.py`** catches it.
3. **`retriever.py`** searches the **FAISS memory**.
4. **FAISS** finds a chunk about cancer.
5. **AI (Groq)** reads that chunk and writes a 2-line summary.
6. **`application.py`** shows that summary on your screen!

**Congratulations! You now understand the entire internal clockwork of a RAG Chatbot!**
