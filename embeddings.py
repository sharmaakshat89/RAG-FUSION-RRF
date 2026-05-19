"""
========================================================
embeddings.py
========================================================

YE FILE RAG PIPELINE KA THIRD LAYER HAI:
EMBEDDING LAYER

Abhi tak humne kya banaya?

TEXT FILE
↓
DOCUMENTS
↓
CHUNKS

Ab next fundamental problem aati hai:

--------------------------------------------------------
PROBLEM:
--------------------------------------------------------

Computer text ka "meaning" directly understand nahi karta.

Uske liye:

"Virat Kohli is a batsman"

sirf characters hain.

Machine ko semantic understanding dene ke liye
text ko numbers me convert karna padta hai.

--------------------------------------------------------
SOLUTION:
--------------------------------------------------------

EMBEDDINGS

Embedding basically:
text ka numerical semantic representation hota hai.

Simple language me:

"text ko mathematical coordinates me convert karna"

========================================================
VERY IMPORTANT INTUITION
========================================================

Imagine ek giant multidimensional semantic universe.

Us universe me:

- cricket related text ek region me
- finance related text dusre region me
- cooking text alag region me

Embedding model ka kaam hota hai:

similar meanings ko semantic space me
close place karna.

Example:

"dog"
and
"puppy"

semantic space me nearby honge.

But:

"dog"
and
"nuclear physics"

bahut door honge.

YAHI semantic search ka foundation hai.

========================================================
MENTAL MODEL
========================================================

Chunks
↓
Embedding model
↓
Vectors
↓
Vector database
↓
Similarity search possible

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Previous layer se chunks import kar rahe hain.
#
# IMPORTANT:
#
# Hum progressively architecture build kar rahe hain.
#
# Har file previous layer ke reusable outputs consume karegi.
#
# Isi approach se real production systems
# modular bante hain.

from chunking import chunks


# OpenAIEmbeddings:
#
# Ye embedding model wrapper hai.
#
# Iska kaam:
#
# text
# ↓
# numerical vectors
#
# convert karna.
#
# IMPORTANT:
#
# Embedding model aur LLM same cheez nahi hote.
#
# LLM:
# text generate karta hai
#
# Embedding model:
# semantic numerical representation banata hai

from langchain_openai import OpenAIEmbeddings


# FAISS:
#
# Facebook AI Similarity Search
#
# Ye vector database / vector index hai.
#
# Iska kaam:
#
# query vector
# vs
# stored vectors
#
# compare karna efficiently.
#
# IMPORTANT:
#
# Agar vectors sirf Python list me store kar diye,
# to search extremely slow ho jayega.
#
# FAISS optimized similarity search provide karta hai.

from langchain_community.vectorstores import FAISS


# OS module:
#
# API keys environment variables se access karne ke liye.

import os


# ======================================================
# API KEY
# ======================================================

# Embedding model OpenAI API use karega.
#
# Isliye API key required hai.
#
# Usually production systems me:
# - .env files
# - secret managers
# - vault systems
#
# use hote hain.
#
# Abhi educational simplicity ke liye
# environment variable use kar rahe hain.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ======================================================
# INITIALIZE EMBEDDING MODEL
# ======================================================

# Yaha actual embedding model initialize ho raha hai.
#
# Ye model internally:
#
# text
# ↓
# tokenization
# ↓
# neural network
# ↓
# vector generation
#
# perform karega.
#
# Example output:
#
# [0.123, -0.882, 0.551, ...]
#
# Ye thousands-dimensional vector ho sakta hai.
#
# IMPORTANT:
#
# Human readable nahi hota.
# Machine-computable representation hota hai.

embedding_model = OpenAIEmbeddings(
    api_key=OPENAI_API_KEY
)


# ======================================================
# CREATE VECTOR STORE
# ======================================================

# YE RAG KA MOST IMPORTANT STEP HAI AB TAK.
#
# Yaha:
#
# chunks
# ↓
# embeddings
# ↓
# vector database
#
# create ho raha hai.
#
# Internally kya ho raha hai?
#
# Step 1:
# Har chunk embedding model ko diya ja raha hai
#
# Step 2:
# Har chunk ka vector generate ho raha hai
#
# Step 3:
# Vector FAISS me store ho raha hai
#
# Step 4:
# Original text bhi mapping ke saath preserve ho raha hai
#
# Final result:
#
# semantic searchable knowledge base

vectorstore = FAISS.from_documents(
    documents=chunks,
    embedding=embedding_model
)


# ======================================================
# DEBUGGING / INSPECTION
# ======================================================

# RAG systems me inspection extremely important hai.
#
# Yaha hum verify karenge:
#
# - vectorstore bana ya nahi
# - embeddings generate hue ya nahi
# - index ready hai ya nahi

print("\n================ VECTOR STORE CREATED ================\n")

print(vectorstore)


# ======================================================
# TEST SEMANTIC SEARCH
# ======================================================

# Ye VERY IMPORTANT educational step hai.
#
# Yaha pehli baar hum semantic retrieval test karenge.
#
# similarity_search():
#
# query ko bhi embedding me convert karta hai
#
# phir:
#
# query embedding
# vs
# stored chunk embeddings
#
# compare karta hai.

test_query = "What is this document about?"


# k=2 matlab:
# top 2 most semantically relevant chunks lao

results = vectorstore.similarity_search(
    test_query,
    k=2
)


print("\n================ TEST QUERY ================\n")

print(test_query)


print("\n================ RETRIEVED CHUNKS ================\n")

for index, result in enumerate(results):

    print(f"\n========== RESULT {index} ==========\n")

    print(result.page_content)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally samjho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne previous layer se:

chunks

import kiye.

Ab hum semantic units ke saath kaam kar rahe the.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

Embedding model initialize hua.

Ye neural network based model hai
jo text ko vectors me convert karta hai.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

FAISS vector store create hua.

Internally:

chunk
↓
embedding vector
↓
stored in vector index

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Ab humare paas:

vectorstore

naam ka reusable semantic database hai.

Later files directly import karenge:

from embeddings import vectorstore

========================================================
MOST IMPORTANT RAG INSIGHT
========================================================

RAG keyword search nahi karta.

Ye:
"meaning similarity"
search karta hai.

Example:

Query:
"football player"

System shayad:
"soccer athlete"

retrieve kar le.

Even exact words absent hone par bhi.

KYUN?

Kyuki embeddings meaning capture karte hain.

========================================================
VERY IMPORTANT DIFFERENCE
========================================================

Traditional Search:
Exact words match karta hai

Semantic Search:
Meaning match karta hai

Yahi embeddings ka actual power hai.

========================================================
PIPELINE STATUS
========================================================

TEXT FILE
↓
DOCUMENTS
↓
CHUNKS
↓
EMBEDDINGS
↓
VECTOR DATABASE

NEXT FILE:

retrieval.py

Waha hum properly retriever layer banayenge
jo user queries ke liye relevant chunks fetch karega.

========================================================
"""