"""
========================================================
api.py
========================================================

YE FILE RAG PIPELINE KA FINAL LAYER HAI:
API SERVING LAYER

Abhi tak humne kya build kiya?

TEXT FILE
↓
DOCUMENTS
↓
CHUNKS
↓
EMBEDDINGS
↓
VECTOR DATABASE
↓
RETRIEVAL
↓
FUSION
↓
PROMPT AUGMENTATION
↓
LLM GENERATION

Ab final question:

--------------------------------------------------------
QUESTION:
--------------------------------------------------------

Is RAG system ko:
- frontend
- mobile app
- chatbot UI
- external applications

kaise use karenge?

Answer:

API

========================================================
VERY IMPORTANT INSIGHT
========================================================

Production AI systems mostly:
HTTP APIs
ke through expose hote hain.

Frontend directly Python functions call nahi karta.

Instead:

Frontend
↓
HTTP Request
↓
API Server
↓
RAG Pipeline
↓
Response

========================================================
MENTAL MODEL
========================================================

User UI
↓
POST request
↓
FastAPI endpoint
↓
run_rag_pipeline()
↓
LLM answer
↓
JSON response

========================================================
VERY IMPORTANT CONCEPT
========================================================

FastAPI:
Python web framework hai.

Ye:
- HTTP requests receive karta hai
- Python functions execute karta hai
- JSON responses return karta hai

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# FastAPI:
#
# Main web framework.
#
# Iske through hum:
# - API endpoints
# - HTTP routes
# - request handling
#
# define karenge.

from fastapi import FastAPI


# BaseModel:
#
# Request body schema validation ke liye.
#
# IMPORTANT:
#
# Ye ONLY minimal allowed class usage hai
# because FastAPI request schemas ke liye
# Pydantic commonly required hota hai.

from pydantic import BaseModel


# Previous orchestration layer import.
#
# Yaha actual intelligence already built hai.
#
# API layer sirf:
# "transport wrapper"
#
# provide karega.

from pipeline import run_rag_pipeline


# ======================================================
# CREATE FASTAPI APP
# ======================================================

# Ye actual API server instance hai.

app = FastAPI()


# ======================================================
# REQUEST SCHEMA
# ======================================================

# API request ka expected JSON structure define kar rahe hain.
#
# Example request:
#
# {
#     "question": "Explain embeddings"
# }
#
# FastAPI automatically:
# - validation
# - parsing
# - schema generation
#
# handle karega.

class QueryRequest(BaseModel):

    question: str


# ======================================================
# ROOT ENDPOINT
# ======================================================

# Basic health-check endpoint.
#
# Browser me:
#
# http://localhost:8000
#
# open karoge to ye response milega.

@app.get("/")
def home():

    return {

        "message": "RAG API is running"
    }


# ======================================================
# MAIN RAG ENDPOINT
# ======================================================

# YEH ACTUAL AI ENDPOINT HAI.
#
# Frontend/apps isi endpoint ko hit karenge.
#
# Endpoint:
#
# POST /ask
#
# Request:
#
# {
#     "question": "What is RAG?"
# }
#
# Response:
#
# {
#     "question": "...",
#     "answer": "..."
# }

@app.post("/ask")
def ask_question(request: QueryRequest):

    # --------------------------------------------------
    # EXTRACT USER QUESTION
    # --------------------------------------------------
    #
    # Request body se actual user query nikal rahe hain.

    user_question = request.question


    print("\n==================================================")
    print("NEW API REQUEST RECEIVED")
    print("==================================================\n")


    print("\n========== USER QUESTION ==========\n")

    print(user_question)


    # --------------------------------------------------
    # RUN COMPLETE RAG PIPELINE
    # --------------------------------------------------
    #
    # IMPORTANT:
    #
    # API layer khud intelligence contain nahi karta.
    #
    # Ye sirf:
    #
    # request
    # ↓
    # pipeline execution
    # ↓
    # response
    #
    # handle karta hai.

    final_answer = run_rag_pipeline(user_question)


    # --------------------------------------------------
    # RETURN JSON RESPONSE
    # --------------------------------------------------
    #
    # FastAPI automatically Python dictionary ko
    # JSON response me convert kar deta hai.

    return {

        "question": user_question,

        "answer": final_answer
    }


# ======================================================
# HOW TO RUN THE SERVER
# ======================================================

# Terminal command:
#
# uvicorn api:app --reload
#
# Explanation:
#
# uvicorn:
# ASGI server
#
# api:
# file name
#
# app:
# FastAPI object
#
# --reload:
# code changes par auto restart


"""
========================================================
HOW TO TEST THE API
========================================================

STEP 1:
Run server

uvicorn api:app --reload

--------------------------------------------------------

STEP 2:
Open browser

http://localhost:8000/docs

--------------------------------------------------------

IMPORTANT:
FastAPI automatically Swagger UI generate karta hai.

Iska matlab:
interactive API testing UI milta hai
without frontend coding.

--------------------------------------------------------

STEP 3:
Test endpoint

POST /ask

Example request:

{
    "question": "Explain embeddings"
}

--------------------------------------------------------

STEP 4:
API internally:

question
↓
run_rag_pipeline()
↓
retrieval
↓
fusion
↓
prompting
↓
LLM
↓
answer

run karega.

========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Frontend/API client ne HTTP request bheji.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

FastAPI ne request receive ki.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

Question extract hui.

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Entire RAG pipeline execute hua.

Internally:

retrieval
↓
fusion
↓
prompt augmentation
↓
LLM generation

--------------------------------------------------------
STEP 5
--------------------------------------------------------

Final answer JSON response ban kar
client ko return hua.

========================================================
MOST IMPORTANT ENGINEERING INSIGHT
========================================================

Production AI systems generally:

"LLM wrappers"

nahi hote.

They are:

DATA PIPELINES
+
RETRIEVAL SYSTEMS
+
ORCHESTRATION LAYERS
+
API SERVERS

========================================================
FINAL COMPLETE MENTAL MODEL
========================================================

PDF / TEXT
↓
INGESTION
↓
DOCUMENTS
↓
CHUNKING
↓
SEMANTIC CHUNKS
↓
EMBEDDINGS
↓
VECTOR DATABASE
↓
RETRIEVAL
↓
FUSION
↓
PROMPT AUGMENTATION
↓
LLM GENERATION
↓
FASTAPI SERVING
↓
HTTP RESPONSE

========================================================
BIGGEST RAG REALIZATION
========================================================

RAG is NOT:

"just using ChatGPT with PDFs"

RAG actually means:

Building a semantic information retrieval system
that feeds grounded context into an LLM.

========================================================
IMPORTANT CAREER INSIGHT
========================================================

Most real AI engineering jobs today involve:
- retrieval systems
- orchestration
- APIs
- pipelines
- data flow
- prompt augmentation

NOT:
training giant models from scratch.

========================================================
END OF MODULAR RAG SERIES
========================================================
"""