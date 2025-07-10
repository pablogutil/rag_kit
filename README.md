# 🧩 RAG Kit

A plug-and-play backend for building your own RAG (Retrieval-Augmented Generation) apps using FastAPI, LangChain, and Qdrant/FAISS.

This is a reusable starting point for any document-based AI system — legal Q&A, medical search, internal product docs, and more.

---

## 🔧 Features

- 📁 Upload documents (PDF, Markdown, etc.)
- 🧠 Chunk & embed with LangChain
- 📦 Store in Qdrant or FAISS
- 🔍 Query with LLM and return contextual answers
- 🚀 Clean FastAPI backend with modular structure

---

## ⚙️ Setup

```bash
git clone https://github.com/yourname/rag-kit.git
cd rag-kit
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
