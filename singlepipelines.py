# ============================================================
# ADVANCED RAG PIPELINE
# ============================================================
#
# FEATURES:
#
# 1. Document Loading
# 2. Chunking
# 3. Embeddings
# 4. Vector Store
# 5. Similarity Search
# 6. MMR Retrieval
# 7. BM25 Retrieval
# 8. Ensemble Retrieval
# 9. RRF (Reciprocal Rank Fusion)
# 10. Context Construction
# 11. LLM Answer Generation
#
# NO OOP
# NO CUSTOM CLASSES
# PURE PROCEDURAL STYLE
#
# ============================================================


# ============================================================
# IMPORTS
# ============================================================

# dotenv -> .env file se API keys load karne ke liye
from dotenv import load_dotenv

# os -> environment variables access karne ke liye
import os

# pprint -> pretty print
from pprint import pprint

# ============================================================
# LANGCHAIN IMPORTS
# ============================================================

# PDF loader
from langchain_community.document_loaders import PyPDFLoader

# Text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OpenAI embeddings
from langchain_openai import OpenAIEmbeddings

# Chroma vector database
from langchain_community.vectorstores import Chroma

# BM25 retriever
from langchain_community.retrievers import BM25Retriever

# Ensemble retriever
from langchain.retrievers import EnsembleRetriever

# OpenAI LLM
from langchain_openai import ChatOpenAI

# Prompt template
from langchain.prompts import ChatPromptTemplate

# ============================================================
# LOAD ENV VARIABLES
# ============================================================

load_dotenv()

# ============================================================
# STEP 1 — LOAD DOCUMENTS
# ============================================================

# YEH RAG KA SABSE PEHLA STEP HAI
#
# RAG begins with KNOWLEDGE.
#
# LLM ko khud sab kuch nahi pata hota.
# Hum usse external information dete hain.
#
# Isliye pehle:
#
# PDF -> Documents
#
# conversion hota hai.


print("\n")
print("=" * 60)
print("STEP 1 — LOADING PDF")
print("=" * 60)

# PDF loader initialize kar rahe hain
loader = PyPDFLoader("attention.pdf")

# PDF ke saare pages load ho jayenge
documents = loader.load()

print(f"\nTotal document pages loaded: {len(documents)}")

# First page dekhte hain
print("\nFIRST DOCUMENT OBJECT:\n")

pprint(documents[0])


# ============================================================
# IMPORTANT MENTAL MODEL
# ============================================================

# Document object usually contains:
#
# 1. page_content
#    -> actual text
#
# 2. metadata
#    -> source
#    -> page number
#    -> filename etc
#
# Metadata later citations aur traceability me help karta hai.


# ============================================================
# STEP 2 — CHUNKING
# ============================================================

print("\n")
print("=" * 60)
print("STEP 2 — CHUNKING")
print("=" * 60)

# IMPORTANT:
#
# Entire PDF ko embed nahi karte.
#
# WHY?
#
# Because:
#
# 1. Very large context
# 2. Retrieval accuracy kharab
# 3. Semantic precision low
#
# Instead:
#
# PDF ko SMALL CHUNKS me todte hain.
#
# This is THE core idea of RAG.
#
# Retrieval happens over:
#
# semantic fragments
#
# not entire files.


splitter = RecursiveCharacterTextSplitter(

    # chunk size
    chunk_size=800,

    # overlap between chunks
    #
    # overlap important hota hai because
    # sentence cut ho sakta hai
    chunk_overlap=150
)

# documents -> chunks
chunks = splitter.split_documents(documents)

print(f"\nTotal chunks created: {len(chunks)}")

print("\nFIRST CHUNK:\n")

print(chunks[0].page_content[:1000])


# ============================================================
# STEP 3 — EMBEDDINGS
# ============================================================

print("\n")
print("=" * 60)
print("STEP 3 — EMBEDDINGS")
print("=" * 60)

# EMBEDDINGS = TEXT -> VECTOR
#
# Human language ko numbers me convert kiya jata hai.
#
# Example:
#
# "dog"
# ->
# [0.213, -0.883, 0.111 ....]
#
# Similar meaning waale texts
# vector space me paas hote hain.
#
# This is semantic search.


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

print("\nEmbedding model initialized.")


# ============================================================
# STEP 4 — VECTOR STORE
# ============================================================

print("\n")
print("=" * 60)
print("STEP 4 — VECTOR DATABASE")
print("=" * 60)

# VECTOR DATABASE stores:
#
# chunk
# +
# embedding vector
#
# So later:
#
# user query
# ->
# embedding
# ->
# nearest semantic chunks


vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("\nVector DB created successfully.")


# ============================================================
# STEP 5 — SIMILARITY RETRIEVER
# ============================================================

print("\n")
print("=" * 60)
print("STEP 5 — SIMILARITY RETRIEVER")
print("=" * 60)

# Basic vector similarity retrieval.
#
# Query embedding
# compared against
# chunk embeddings.
#
# Most semantically similar chunks return hote hain.


similarity_retriever = vectorstore.as_retriever(

    search_type="similarity",

    search_kwargs={
        "k": 5
    }
)

print("\nSimilarity retriever ready.")


# ============================================================
# STEP 6 — MMR RETRIEVER
# ============================================================

print("\n")
print("=" * 60)
print("STEP 6 — MMR RETRIEVER")
print("=" * 60)

# MMR = Maximal Marginal Relevance
#
# THIS IS EXTREMELY IMPORTANT.
#
# Normal similarity retrieval problem:
#
# saare chunks almost same aa sakte hain.
#
# Example:
#
# Chunk 1 -> cats
# Chunk 2 -> cats
# Chunk 3 -> cats
#
# diversity nahi hoti.
#
# MMR solves this.
#
# MMR balances:
#
# 1. relevance
# 2. diversity
#
# Formula intuition:
#
# Final Score =
#
# relevance
# -
# redundancy
#
# So:
#
# highly relevant
# but DIFFERENT chunks
# retrieve hote hain.


mmr_retriever = vectorstore.as_retriever(

    search_type="mmr",

    search_kwargs={

        # final returned docs
        "k": 5,

        # candidate pool
        #
        # pehle 20 candidates laega
        # fir diversity optimize karega
        "fetch_k": 20,

        # diversity strength
        #
        # 1 -> more relevance
        # 0 -> more diversity
        "lambda_mult": 0.5
    }
)

print("\nMMR retriever ready.")


# ============================================================
# STEP 7 — BM25 RETRIEVER
# ============================================================

print("\n")
print("=" * 60)
print("STEP 7 — BM25 RETRIEVER")
print("=" * 60)

# BM25 is OLD SCHOOL lexical search.
#
# This is NOT semantic.
#
# It works on:
#
# exact keywords
#
# Example:
#
# Query:
# "transformer architecture"
#
# BM25 checks:
#
# exact occurrence frequency
#
# WHY IMPORTANT?
#
# Semantic search kabhi exact keyword miss kar deta hai.
#
# BM25 exact terms pakad leta hai.
#
# Best systems combine:
#
# semantic + lexical


bm25_retriever = BM25Retriever.from_documents(chunks)

bm25_retriever.k = 5

print("\nBM25 retriever ready.")


# ============================================================
# STEP 8 — ENSEMBLE RETRIEVER
# ============================================================

print("\n")
print("=" * 60)
print("STEP 8 — ENSEMBLE RETRIEVAL")
print("=" * 60)

# Ensemble retrieval means:
#
# multiple retrievers together.
#
# WHY?
#
# Every retriever has strengths and weaknesses.
#
# Vector search:
# good semantics
#
# BM25:
# good exact keywords
#
# MMR:
# good diversity
#
# Together:
# stronger retrieval quality


ensemble_retriever = EnsembleRetriever(

    retrievers=[
        bm25_retriever,
        similarity_retriever,
        mmr_retriever
    ],

    # weights for each retriever
    weights=[0.3, 0.3, 0.4]
)

print("\nEnsemble retriever ready.")


# ============================================================
# STEP 9 — USER QUERY
# ============================================================

print("\n")
print("=" * 60)
print("STEP 9 — USER QUERY")
print("=" * 60)

query = "What causes attention fragmentation?"

print(f"\nUser Query:\n{query}")


# ============================================================
# STEP 10 — RETRIEVE DOCUMENTS
# ============================================================

print("\n")
print("=" * 60)
print("STEP 10 — RETRIEVAL")
print("=" * 60)

# Ensemble retriever internally:
#
# 1. runs multiple retrievers
# 2. merges results
# 3. reranks
#
# This improves recall significantly.


retrieved_docs = ensemble_retriever.invoke(query)

print(f"\nRetrieved docs count: {len(retrieved_docs)}")


# ============================================================
# STEP 11 — MANUAL RRF UNDERSTANDING
# ============================================================

print("\n")
print("=" * 60)
print("STEP 11 — RRF (RECIPROCAL RANK FUSION)")
print("=" * 60)

# IMPORTANT CONCEPT
#
# RRF = Reciprocal Rank Fusion
#
# Used in advanced retrieval systems.
#
# IDEA:
#
# If a document ranks well across MANY retrievers,
# then it is probably important.
#
#
# Formula intuition:
#
# score += 1 / (k + rank)
#
# rank 1 gets higher score.
#
# lower ranks get lower contribution.
#
#
# WHY POWERFUL?
#
# Because:
#
# even if retrievers disagree,
# consensus documents rise upward.
#
#
# Modern search systems heavily use fusion strategies.


# Let's manually inspect rankings

print("\nSIMILARITY RETRIEVER RESULTS:\n")

sim_docs = similarity_retriever.invoke(query)

for i, doc in enumerate(sim_docs):
    print(f"\nRank {i+1}")
    print(doc.page_content[:200])



print("\n")
print("=" * 60)

print("\nMMR RETRIEVER RESULTS:\n")

mmr_docs = mmr_retriever.invoke(query)

for i, doc in enumerate(mmr_docs):
    print(f"\nRank {i+1}")
    print(doc.page_content[:200])



print("\n")
print("=" * 60)

print("\nBM25 RETRIEVER RESULTS:\n")

bm25_docs = bm25_retriever.invoke(query)

for i, doc in enumerate(bm25_docs):
    print(f"\nRank {i+1}")
    print(doc.page_content[:200])


# ============================================================
# STEP 12 — CONTEXT BUILDING
# ============================================================

print("\n")
print("=" * 60)
print("STEP 12 — CONTEXT CONSTRUCTION")
print("=" * 60)

# Retrieved chunks ko combine karke
# final context banaya jata hai.


context = "\n\n".join(

    [doc.page_content for doc in retrieved_docs]
)

print("\nContext length built successfully.")


# ============================================================
# STEP 13 — PROMPT TEMPLATE
# ============================================================

print("\n")
print("=" * 60)
print("STEP 13 — PROMPT TEMPLATE")
print("=" * 60)

# RAG ka FINAL MAGIC:
#
# retrieved knowledge
# +
# user query
#
# injected into prompt


prompt = ChatPromptTemplate.from_template("""

You are a helpful AI assistant.

Answer ONLY from the provided context.

If answer is not present,
say:
"I could not find this in the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:

""")


# ============================================================
# STEP 14 — LLM
# ============================================================

print("\n")
print("=" * 60)
print("STEP 14 — LLM INITIALIZATION")
print("=" * 60)

llm = ChatOpenAI(

    model="gpt-4.1-mini",

    temperature=0
)

print("\nLLM initialized.")


# ============================================================
# STEP 15 — FINAL PROMPT
# ============================================================

print("\n")
print("=" * 60)
print("STEP 15 — FINAL PROMPT")
print("=" * 60)

final_prompt = prompt.format(

    context=context,
    question=query
)

print("\nPrompt built successfully.")


# ============================================================
# STEP 16 — GENERATE ANSWER
# ============================================================

print("\n")
print("=" * 60)
print("STEP 16 — GENERATING ANSWER")
print("=" * 60)

response = llm.invoke(final_prompt)

print("\nFINAL ANSWER:\n")

print(response.content)


# ============================================================
# FINAL MENTAL MODEL
# ============================================================

#
# RAW PDF
#     ↓
# DOCUMENTS
#     ↓
# CHUNKS
#     ↓
# EMBEDDINGS
#     ↓
# VECTOR DB
#     ↓
# MULTIPLE RETRIEVERS
#     ↓
# MMR + BM25 + VECTOR SEARCH
#     ↓
# ENSEMBLE / RRF STYLE FUSION
#     ↓
# BEST CONTEXT
#     ↓
# PROMPT AUGMENTATION
#     ↓
# LLM RESPONSE
#
#
# THIS IS MODERN RAG.
#
# ============================================================