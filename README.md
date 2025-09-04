# 🎥 Video Processor with LLM-Based Highlight Extraction

## Before we start
Before starting, please read the submission document with some background and explanations called EdmondChalom_submission_070325.docx, sent separately by e-mail.

## Overview

This project:
✅ Accepts `.mp4` videos  
✅ Extracts key moments (explosions, people speaking, vehicle movement)  
✅ Transcribes speech with an older vosk-model  
✅ Generates embeddings using Transformers  
✅ Stores highlights in PostgreSQL with pgvector  
✅ Supports similarity-based retrieval for finding moments

## Running in GitHub Codespaces or gitpod

Before running, please make sure you read the file EdmondChalom_submission_070325.docx
1️⃣ Push this repository to your GitHub.  
2️⃣ Open in Codespaces or gitpod (tested only on gitpod).  
3️⃣ Ensure the mp4 files are in the root of the repository.  
4️⃣ Build and run:

```bash
docker-compose up --build
