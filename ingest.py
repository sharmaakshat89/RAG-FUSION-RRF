"""
========================================================
ingest.py
========================================================

YE FILE RAG PIPELINE KA SABSE PEHLA LAYER HAI:
INGESTION LAYER

RAG pipeline kabhi embeddings se start nahi hoti.
Na vector DB se.
Na LLM se.

Sabse pehle system ko KNOWLEDGE chahiye hota hai.

Aur ingestion layer ka kaam hota hai:

    "Raw external data ko Python-readable documents me convert karna"

Ye data ho sakta hai:
- PDF
- TXT
- DOCX
- Website
- Database rows
- CSV
- APIs

Abhi hum uploaded pipeline ke according text/PDF style
documents ingest karenge.

--------------------------------------------------------
MENTAL MODEL
--------------------------------------------------------

REAL WORLD:
PDF file ya text file
↓
LangChain Loader
↓
Document objects
↓
Python memory

Ye "Document" objects later:
- chunk honge
- embeddings banenge
- vector DB me jayenge
- retrieve honge

IMPORTANT:

Is stage par:
❌ embeddings nahi
❌ vector DB nahi
❌ retrieval nahi

Sirf KNOWLEDGE KO SYSTEM KE ANDAR LANA hai.

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# TextLoader:
# Ye simple text files ko load karta hai
# and unhe LangChain Document objects me convert karta hai

from langchain_community.document_loaders import TextLoader


# Pathlib:
# File paths safely handle karne ke liye
# Better than raw string paths

from pathlib import Path


# ======================================================
# FILE PATH
# ======================================================

# Yaha hum source knowledge define kar rahe hain
#
# RAG systems me "knowledge source"
# bahut important concept hota hai.
#
# Ye wahi information hai jiske basis par
# future me AI answers generate karega.
#
# Agar source garbage hua,
# to retrieval bhi garbage hoga.
#
# "Garbage in → garbage out"

DATA_PATH = Path("data/sample.txt")


# ======================================================
# LOADER INITIALIZATION
# ======================================================

# Loader ka kaam:
#
# File ko open karna
# ↓
# Text extract karna
# ↓
# Usko structured Document objects me convert karna
#
# IMPORTANT:
#
# LangChain mostly raw strings pe kaam nahi karta.
#
# Wo "Document" abstraction use karta hai.
#
# Kyun?
#
# Kyunki later stages me sirf text nahi,
# metadata bhi important hota hai.
#
# Example metadata:
# - source file
# - page number
# - author
# - timestamp
#
# Retrieval systems metadata heavily use karte hain.

loader = TextLoader(str(DATA_PATH))


# ======================================================
# LOAD DOCUMENTS
# ======================================================

# Ye MOST IMPORTANT STEP hai ingestion layer ka.
#
# load() karte hi:
#
# File system
# ↓
# Raw text
# ↓
# LangChain Document objects
#
# Convert ho jata hai.
#
# Output usually LIST hota hai.
#
# Example:
#
# [
#     Document(
#         page_content="some text...",
#         metadata={"source": "..."}
#     )
# ]
#
# IMPORTANT:
#
# Even ek single file bhi LIST me aati hai.
#
# Kyunki future me:
# - multiple PDFs
# - multiple text files
# - multiple sources
#
# handle karna common hota hai.

documents = loader.load()


# ======================================================
# DEBUG / INSPECTION
# ======================================================

# RAG build karte waqt
# har stage inspect karna extremely important hota hai.
#
# Beginners mostly blindly pipelines run karte hain.
#
# Production engineers har layer verify karte hain.
#
# Yaha hum dekh rahe hain:
#
# - Kitne documents load hue
# - Actual content kya hai
# - Metadata kya hai

print("\n================ DOCUMENT COUNT ================\n")

print(len(documents))


print("\n================ FIRST DOCUMENT ================\n")

print(documents[0])


print("\n================ PAGE CONTENT ================\n")

print(documents[0].page_content)


print("\n================ METADATA ================\n")

print(documents[0].metadata)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

Step-by-step mentally samjho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne ek raw file point ki:

    data/sample.txt

Abhi tak ye sirf filesystem me stored data tha.

LLM isko directly access nahi kar sakta.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

TextLoader use hua.

Ye loader:
- file open karta hai
- encoding handle karta hai
- text extract karta hai

--------------------------------------------------------
STEP 3
--------------------------------------------------------

load() call hua.

Aur raw text convert ho gaya:

RAW TEXT
↓
Document object

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Ab humare paas:

documents

naam ki LIST hai.

Ye RAG pipeline ka FIRST reusable artifact hai.

Later files isko import karenge:

from ingest import documents

Aur isi modular architecture se
pipeline gradually evolve hogi.

========================================================
VERY IMPORTANT MENTAL MODEL
========================================================

Abhi humne AI nahi banayi.

Humne bas:

"knowledge ko machine-readable form me ingest kiya"

RAG ka FIRST principle:

LLM ko knowledge khilani padti hai.

========================================================
PIPELINE STATUS
========================================================

CURRENT:

TEXT FILE
↓
DOCUMENT OBJECTS

NEXT FILE:

chunking.py

Waha hum seekhenge:

documents
↓
small semantic chunks

Kyunki embeddings directly giant documents par
efficiently kaam nahi karti.

========================================================
"""