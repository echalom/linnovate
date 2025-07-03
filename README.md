# 🎥 Video Processor with LLM-Based Highlight Extraction

## Overview

This project:
✅ Accepts `.mp4` videos  
✅ Extracts key moments (explosions, people speaking, vehicle movement)  
✅ Transcribes speech with an older vosk-model  
✅ Generates embeddings using Transformers  
✅ Stores highlights in PostgreSQL with pgvector  
✅ Supports similarity-based retrieval for finding moments

## Running in GitHub Codespaces or gitpod

1️⃣ Push this repository to your GitHub.  
2️⃣ Open in Codespaces or gitpod (tested only on gitpod).  
3️⃣ Ensure the mp4 files are in the root of the repository.  
4️⃣ Build and run:

```bash
docker-compose up --build
