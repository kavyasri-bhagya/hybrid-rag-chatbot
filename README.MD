#  Hybrid RAG Chatbot

This project is a **Hybrid Retrieval-Augmented Generation (RAG) system** that combines **BM25 keyword search + Dense vector search (pgvector) + Google Gemini LLM** to answer questions from PDF documents.

---

# Features

-  PDF ingestion and text extraction
-  Chunking of documents
-  Embeddings using Google Gemini (`gemini-embedding-001`)
-  Vector storage using PostgreSQL + pgvector
-  Hybrid search:
  - BM25 (keyword-based search)
  - Dense vector similarity search
-  Reciprocal Rank Fusion (RRF) for ranking
-  Answer generation using Gemini (`gemini-2.5-flash`)
-  Chatbot interface for Q&A

---

# Architecture Flow

PDFs → Text Extraction → Chunking → Embeddings  
→ PostgreSQL (Vector DB)  
→ BM25 Index + Dense Search  
→ Hybrid Fusion (RRF)  
→ Gemini LLM → Final Answer

---

# Project Structure
