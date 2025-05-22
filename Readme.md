# Curion – A Personalized AI Mentor (Prototype)

**Curion** is a terminal-based AI mentor designed to act as your philosophical and intellectual companion. This prototype uses local LLMs, embeddings, and memory to generate contextual, metaphorical, and thoughtful responses — all optimized to work efficiently even on lower-end machines.

---

## ✨ Features

* 🤖 **LLM-Powered Responses** — Uses `gemma3:4b` via [Ollama](https://ollama.com/) for lightweight, fast, local inference.
* 🧠 **Knowledge Ingestion** — Adds external text to a vector store with embeddings for context-aware answers.
* 🤩 **Memory-Based Personalization** — Tracks previous questions and interests to customize replies.
* ⚡ **Streaming Output** — CLI displays output in real-time using `rich`.
* 💬 **Socratic Prompting** — Answers are styled like a mentor: metaphorical, curious, and reflective.

---

## 📦 Requirements

To run Curion locally, you’ll need:

* Python 3.10+
* [Ollama](https://ollama.com/) installed on your local machine
* A local model like `gemma:4b` pulled via Ollama
* Git (optional for cloning)

### Install Dependencies

```bash
pip install langchain langchain_ollama langchain_chroma chromadb rich
```

---

## 🚀 Getting Started

### 1. Clone or Fork the Repository

```bash
git clone https://github.com/your-username/curion.git
cd curion
```

### 2. Install and Set Up Ollama

Download and install [Ollama](https://ollama.com/) if you haven’t already:

```bash
ollama pull gemma:4b
```

> You can use any model that works with Ollama — more on that in the config section.

### 3. Run Curion

```bash
python cli_interface.py
```

Curion will greet you in the terminal and await your question.

---

## ⚙️ Configuration & Performance Customization

Curion is designed to run efficiently on most devices, but you can **tweak every part** of it for better performance, more personalization, or deeper responses.

### 🔹 1. **LLM Model** (`gemma3:4b`)

**Why it's used**:

* Lightweight, fast, and good for most philosophical/reflective tasks
* Works well on low to mid-spec machines

**Change it if**:

* You want more creative, technical, or verbose responses
* You have a stronger GPU or CPU

**How**:
In `cli_interface.py` and `brain.py`, change:

```python
model="gemma3:4b"
```

To any other Ollama-supported model, such as:

* `llama3:8b`
* `mistral:7b-instruct`
* `phi:2` (for ultra-fast inference)

---

### 🔹 2. **Streaming Output** (`stream=True`)

**Why it matters**:
Streaming response chunks as they’re generated allows for:

* Faster feedback
* A dynamic, "typing" experience
* Lower wait time for long answers

**Keep it on** for the best CLI experience. Turn off only if you need full output all at once (e.g., for logging).

---

### 🔹 3. **Context Summarization**

**Purpose**:
Summarizing the context before sending it to the LLM makes the prompt shorter and **faster** to process.

**How it helps**:

* Speeds up generation time
* Keeps prompts relevant
* Reduces token overload on smaller models

**Tweak**:

* You can **remove summarization** if you prefer raw knowledge being passed, or
* Add more **contextual data** (e.g., long memory, past queries) for richer responses

---

### 🔹 4. **Embedding Model** (`all-minilm:l6-v2`)

**Why this model?**

* Super fast
* Decent for most conversational embeddings
* Great for local use

**Change it if**:

* You want more accurate, deeply semantic context matching
* You’re okay with slower vector search

**How**:
In `brain.py`, change:

```python
self.embeddings = OllamaEmbeddings(model="all-minilm:l6-v2")
```

To:

```python
self.embeddings = OllamaEmbeddings(model="bge-small" or "instructor-xl")
```

---

### 🔹 5. **Chunk Size & Overlap** (`chunk_size=600`)

**What it does**:
Controls how much text is split into "chunks" for embeddings and vector storage.

* **Smaller chunks** = faster processing, less context depth
* **Larger chunks** = more coherent meaning, but slower

**Defaults**:

```python
chunk_size = 600
chunk_overlap = 100
```

**Tweak it if**:

* You're on a high-performance machine → increase to 1000+
* You're on low RAM/CPU → decrease to 400–500

---

### 🔹 6. **Prompt Structure**

**How Curion prompts the model**:

* Includes your last 3 questions
* Adds a user summary (from memory)
* Summarizes the relevant context
* Styles the AI as a wise, metaphorical mentor

**You can customize**:

* The tone (change "Socratic" to "humorous", "technical", etc.)
* Add goals, emotions, current mood for more personalization
* Use custom instruction sets for specific tasks (like coding help, therapy, tutoring, etc.)

---

### 🛠️ Summary: Who Should Tweak What?

| User Type                  | Recommended Tweaks                                                       |
| -------------------------- | ------------------------------------------------------------------------ |
| ⚡ Beginner/Basic Hardware  | Stick with defaults: Gemma 4B + MiniLM + chunk size 600                  |
| 🔥 Power Users             | Try LLaMA 3 / Mistral, increase chunk size, use BGE embeddings           |
| 🎯 Personalization Seekers | Edit prompt to include user traits, interests, learning styles           |
| 🧪 Experimenters           | Test different embedding models, context amounts, and streaming settings |

---

## 📁 Project Structure

```
.
├── brain.py           # Handles embeddings, vector storage, and summarization
├── cli_interface.py   # The main CLI interaction logic
├── memory.py          # Stores user profile, history, interests
├── data/              # Directory for ChromaDB (vector database)
└── user_profiles/     # Where individual user memory is saved
```

---

## 📣 Feedback & Contributions

This is a prototype — made for fun, learning, and experimentation.
If you have ideas, suggestions, or want to turn Curion into a GUI app, chatbot, or full learning assistant — fork it, play with it, and feel free to open an issue or pull request!

---

## 🧠 Credits

Built by **Abir** — because learning should feel like mentorship, not just search.
Powered by: LangChain • Ollama • Open Models

---
