"""
========================================================
retrieval.py
========================================================

YE FILE RAG PIPELINE KA FOURTH LAYER HAI:
RETRIEVAL LAYER

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

Ab next question:

--------------------------------------------------------
QUESTION:
--------------------------------------------------------

User query aayegi to:
relevant chunks kaise milenge?

Yahi retrieval layer ka kaam hai.

========================================================
IMPORTANT INSIGHT
========================================================

RAG ka REAL intelligence retrieval quality me hota hai.

Agar retrieval weak hua:
- wrong context aayega
- hallucinations badhenge
- answer irrelevant hoga

LLM utna hi intelligent dikhega
jitna relevant context retrieve hoga.

========================================================
MENTAL MODEL
========================================================

User Query
↓
Query Embedding
↓
Similarity Search
↓
Top Relevant Chunks
↓
Context for LLM

========================================================
VERY IMPORTANT CONCEPT
========================================================

Retriever:
LLM nahi hota.

Retriever ka kaam sirf:
"relevant information fetch karna"

Generation baad me hoti hai.

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Previous layer se vectorstore import kar rahe hain.
#
# Is vectorstore ke andar:
#
# - chunk embeddings
# - original chunks
# - similarity index
#
# already stored hai.

from embeddings import vectorstore


# ======================================================
# CREATE RETRIEVER
# ======================================================

# Vector DB directly similarity search kar sakta hai.
#
# But production-style RAG pipelines usually:
#
# vectorstore
# ↓
# retriever abstraction
#
# use karte hain.
#
# Kyun?
#
# Kyunki retriever:
#
# - retrieval interface standardize karta hai
# - search parameters encapsulate karta hai
# - future me multiple retrieval strategies allow karta hai
#
# IMPORTANT:
#
# Retriever ka kaam:
# "relevant chunks lana"
#
# Bas.

retriever = vectorstore.as_retriever(

    # --------------------------------------------------
    # search_type
    # --------------------------------------------------
    #
    # similarity:
    #
    # query embedding
    # vs
    # chunk embeddings
    #
    # similarity compare karega.
    #
    # Most common semantic retrieval strategy.

    search_type="similarity",


    # --------------------------------------------------
    # search_kwargs
    # --------------------------------------------------
    #
    # Retrieval configuration parameters.
    #
    # k:
    # kitne top chunks retrieve karne hain.
    #
    # Bahut low:
    # context miss ho sakta hai
    #
    # Bahut high:
    # noisy irrelevant context aa sakta hai

    search_kwargs={"k": 3}
)


# ======================================================
# USER QUERY
# ======================================================

# Real RAG systems me ye:
#
# - API request
# - chatbot input
# - UI textbox
#
# se aati hai.
#
# Abhi manually test query use kar rahe hain.

query = "Explain the main topic of the document"


# ======================================================
# RETRIEVE RELEVANT CHUNKS
# ======================================================

# YAHI actual semantic retrieval moment hai.
#
# Internally kya ho raha hai?
#
# STEP 1:
# User query embedding me convert hoti hai
#
# STEP 2:
# Query vector compare hota hai
# stored chunk vectors ke against
#
# STEP 3:
# Most semantically similar chunks retrieve hote hain
#
# IMPORTANT:
#
# Ye keyword search nahi hai.
#
# Semantic similarity search hai.

retrieved_docs = retriever.invoke(query)


# ======================================================
# DEBUGGING / INSPECTION
# ======================================================

# Retrieval inspect karna extremely important hai.
#
# Real-world RAG debugging mostly retrieval quality
# inspect karne me hi jaata hai.
#
# Verify:
#
# - relevant chunks aaye?
# - irrelevant noise to nahi?
# - chunk count sahi hai?
# - semantic matching working hai?

print("\n================ USER QUERY ================\n")

print(query)


print("\n================ RETRIEVED DOCUMENT COUNT ================\n")

print(len(retrieved_docs))


print("\n================ RETRIEVED CHUNKS ================\n")

for index, doc in enumerate(retrieved_docs):

    print(f"\n========== RETRIEVED CHUNK {index} ==========\n")

    print(doc.page_content)


# ======================================================
# OPTIONAL: VIEW METADATA
# ======================================================

# Metadata retrieval debugging me extremely useful hota hai.
#
# Isse pata chalta hai:
#
# - chunk kis source se aaya
# - lineage kya hai
# - retrieval consistency kaisi hai

print("\n================ METADATA ================\n")

for index, doc in enumerate(retrieved_docs):

    print(f"\n========== CHUNK {index} METADATA ==========\n")

    print(doc.metadata)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne previous layer se:

vectorstore

import kiya.

Uske andar already:
- chunk embeddings
- semantic index
- chunk mappings

stored the.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

Humne retriever abstraction create kiya.

Retriever basically semantic search interface hai.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

User query aayi:

"Explain the main topic of the document"

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Internally:

query
↓
query embedding
↓
similarity comparison
↓
top matching chunk retrieval

hua.

--------------------------------------------------------
STEP 5
--------------------------------------------------------

Output me:
retrieved_docs

mile.

IMPORTANT:

Ye final answer nahi hai.

Ye sirf:
"relevant context"

hai.

========================================================
MOST IMPORTANT RAG INSIGHT
========================================================

Retriever ka kaam answer generate karna nahi hota.

Retriever ka kaam hota hai:

"LLM ko sahi information dena"

LLM later:
- summarize karega
- explain karega
- synthesize karega

But retrieval determines:
whether answer grounded hoga ya hallucinated.

========================================================
WHY RETRIEVAL QUALITY MATTERS
========================================================

Agar wrong chunks retrieve hue:

Even GPT-5 bhi confidently wrong answer de sakta hai.

Because:

LLM generally retrieved context trust karta hai.

Isliye advanced RAG engineering mostly:
retrieval optimization ka game hai.

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
↓
RETRIEVAL

NEXT FILE:

fusion.py

Waha hum seekhenge:
multiple retrieval results ko combine/rerank
kaise kiya jata hai.

========================================================
"""