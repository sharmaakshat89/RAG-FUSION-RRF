"""
========================================================
chunking.py
========================================================

YE FILE RAG PIPELINE KA SECOND LAYER HAI:
CHUNKING LAYER

Abhi tak humne kya kiya tha?

TEXT FILE
↓
Document objects

Ab next problem aati hai:

--------------------------------------------------------
PROBLEM:
--------------------------------------------------------

LLMs aur embeddings giant documents ko efficiently
handle nahi karte.

Agar poora PDF ek hi embedding me daal diya:
- retrieval weak ho jayega
- irrelevant context aa jayega
- semantic precision kharab ho jayegi

Example:

100-page PDF ka ek single embedding banana
matlab:
- saari meanings mix ho jayengi
- retrieval blurry ho jayega

Ye exactly waise hai jaise:
poori library ko ek hi paragraph me summarize karna.

--------------------------------------------------------
SOLUTION:
--------------------------------------------------------

DOCUMENTS
↓
SMALL SEMANTIC PIECES
(CHUNKS)

Ye chunks later:
- embed honge
- vector DB me store honge
- retrieve honge

IMPORTANT INSIGHT:

RAG retrieval FILE LEVEL par nahi hota.
RAG retrieval CHUNK LEVEL par hota hai.

Ye bahut bada mental shift hai.

========================================================
MENTAL MODEL
========================================================

Large document
↓
split into smaller meaning units
↓
each chunk gets embedding
↓
retrieval becomes precise

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Hum previous layer se reusable output import kar rahe hain.
#
# IMPORTANT:
#
# Yahi modular architecture ka beginning hai.
#
# Instead of rewriting ingestion logic again,
# hum directly previous layer ka output use karenge.
#
# Real-world backend systems exactly isi tarah layered hote hain.

from ingest import documents


# RecursiveCharacterTextSplitter:
#
# Ye LangChain ka text splitter hai.
#
# Iska kaam:
# large text ko intelligently small chunks me todna.
#
# "Recursive" naam kyun?
#
# Kyunki ye multiple separator strategies try karta hai:
#
# paragraph
# ↓
# newline
# ↓
# sentence
# ↓
# spaces
# ↓
# raw characters
#
# Goal:
# possible ho to semantic structure preserve rahe.

from langchain_text_splitters import RecursiveCharacterTextSplitter


# ======================================================
# TEXT SPLITTER CONFIGURATION
# ======================================================

# Chunking RAG ka MOST IMPORTANT tuning layer hota hai.
#
# Yaha do critical parameters hote hain:
#
# 1. chunk_size
# 2. chunk_overlap

text_splitter = RecursiveCharacterTextSplitter(

    # --------------------------------------------------
    # chunk_size
    # --------------------------------------------------
    #
    # Ek chunk me maximum kitne characters honge.
    #
    # Small chunks:
    # + precise retrieval
    # - less context
    #
    # Large chunks:
    # + more context
    # - noisy retrieval
    #
    # Ye balance game hota hai.

    chunk_size=500,


    # --------------------------------------------------
    # chunk_overlap
    # --------------------------------------------------
    #
    # Adjacent chunks ke beech overlap.
    #
    # Kyun important?
    #
    # Imagine:
    #
    # Chunk 1:
    # "Virat Kohli scored..."
    #
    # Chunk 2:
    # "...a century in finals"
    #
    # Agar overlap nahi hua,
    # semantic meaning break ho sakta hai.
    #
    # Overlap context continuity preserve karta hai.

    chunk_overlap=100,
)


# ======================================================
# CREATE CHUNKS
# ======================================================

# Ab actual splitting ho raha hai.
#
# INPUT:
# Document objects
#
# OUTPUT:
# Smaller Document objects
#
# IMPORTANT:
#
# Chunking raw strings return nahi karta.
#
# Har chunk bhi Document object hi hota hai.
#
# Kyun?
#
# Metadata preserve karna hota hai.
#
# Example:
# - original source
# - page info
# - chunk lineage
#
# Ye retrieval debugging me extremely useful hota hai.

chunks = text_splitter.split_documents(documents)


# ======================================================
# DEBUGGING / INSPECTION
# ======================================================

# Production RAG engineers har stage inspect karte hain.
#
# Chunking blindly nahi karni chahiye.
#
# Verify:
# - chunk count
# - chunk size
# - overlap behavior
# - metadata propagation

print("\n================ TOTAL CHUNKS ================\n")

print(len(chunks))


print("\n================ FIRST CHUNK ================\n")

print(chunks[0])


print("\n================ FIRST CHUNK CONTENT ================\n")

print(chunks[0].page_content)


print("\n================ FIRST CHUNK METADATA ================\n")

print(chunks[0].metadata)


# ======================================================
# OPTIONAL: VIEW MULTIPLE CHUNKS
# ======================================================

# Ye bahut educational step hai.
#
# Isse visually samajh aata hai:
# text actually kaise split hua.
#
# Real-world RAG debugging me
# chunk visualization bahut common hota hai.

for index, chunk in enumerate(chunks[:3]):

    print(f"\n================ CHUNK {index} ================\n")

    print(chunk.page_content)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne previous layer se import kiya:

documents

Ye already machine-readable form me the.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

RecursiveCharacterTextSplitter initialize hua.

Ye splitting strategy define karta hai.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

split_documents() run hua.

Aur large documents transform ho gaye:

DOCUMENTS
↓
SMALLER DOCUMENTS

IMPORTANT:

Chunks bhi Document objects hi hain.

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Ab humare paas:

chunks

naam ka reusable pipeline artifact hai.

Later files import karenge:

from chunking import chunks

========================================================
MOST IMPORTANT RAG INSIGHT
========================================================

Embeddings usually:
❌ full books par nahi
❌ giant PDFs par nahi

Instead:

✅ semantic chunks par banti hain

Kyun?

Kyuki retrieval ka goal hota hai:

"query ke relevant SMALL information units find karna"

NOT:
"entire documents retrieve karna"

========================================================
PIPELINE STATUS
========================================================

TEXT FILE
↓
DOCUMENTS
↓
CHUNKS

NEXT FILE:

embeddings.py

Waha hum seekhenge:

chunks
↓
numerical semantic vectors

Aur first time:
semantic search ka actual magic start hoga.

========================================================
"""