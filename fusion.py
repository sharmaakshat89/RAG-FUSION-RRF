"""
========================================================
fusion.py
========================================================

YE FILE RAG PIPELINE KA FIFTH LAYER HAI:
FUSION / ENSEMBLE RETRIEVAL LAYER

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

Ab next important problem:

--------------------------------------------------------
PROBLEM:
--------------------------------------------------------

Single retrieval strategy kabhi kabhi:
- relevant chunk miss kar deti hai
- wording variations miss kar deti hai
- semantic ambiguity me weak ho sakti hai

Example:

User query:
"How does the system store memory?"

Possible relevant document wording:
- persistence layer
- storage architecture
- state management
- database caching

Single query phrasing sometimes enough nahi hoti.

========================================================
SOLUTION:
========================================================

MULTIPLE RETRIEVAL PERSPECTIVES
↓
COMBINE RESULTS
↓
BETTER RECALL

Isko broadly:
- Fusion Retrieval
- Ensemble Retrieval
- Multi-query Retrieval

bola jata hai.

========================================================
VERY IMPORTANT INTUITION
========================================================

Ek hi question ko multiple tariko se poochne par
different chunks retrieve ho sakte hain.

Fusion ka goal hota hai:

"multiple semantic search attempts combine karna"

taaki retrieval quality improve ho.

========================================================
MENTAL MODEL
========================================================

Original Query
↓
Multiple Query Variations
↓
Multiple Retrieval Passes
↓
Merge Results
↓
Deduplicate
↓
Better Context Coverage

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Previous retrieval layer se retriever import kar rahe hain.
#
# IMPORTANT:
#
# Fusion khud retrieval replace nahi karta.
#
# Fusion:
# retrieval ke upar ek orchestration layer hota hai.

from retrieval import retriever


# ======================================================
# USER QUERY
# ======================================================

# Original user query.
#
# Real-world systems me:
# ye chatbot/API/UI se aayegi.

original_query = "How does the RAG system work?"


# ======================================================
# QUERY VARIATIONS
# ======================================================

# Yaha hum manually multiple semantic variations bana rahe hain.
#
# IMPORTANT:
#
# Different wording
# → different embedding vectors
# → different retrieval results
#
# Ye retrieval recall improve karta hai.
#
# Production systems me kabhi:
# - LLM generated reformulations
# - HyDE
# - query rewriting
# - decomposition
#
# bhi use hote hain.
#
# Lekin hum uploaded implementation faithful rakh rahe hain:
# simple procedural multi-query fusion.

queries = [

    original_query,

    "Explain the retrieval pipeline",

    "How does document search happen?",

    "Describe semantic retrieval system",

    "How are embeddings used in RAG?"
]


# ======================================================
# STORE ALL RETRIEVED RESULTS
# ======================================================

# Yaha hum saare retrieval outputs accumulate karenge.

all_retrieved_docs = []


# ======================================================
# MULTI-QUERY RETRIEVAL
# ======================================================

# Har query variation ke liye:
#
# semantic retrieval run hoga.
#
# IMPORTANT:
#
# Ye exactly wahi retriever hai
# jo previous file me banaya tha.
#
# Bas ab:
# ek query ke instead
# multiple retrieval passes ho rahe hain.

for query in queries:

    print(f"\n================ QUERY =================\n")

    print(query)


    # --------------------------------------------------
    # RETRIEVE DOCUMENTS
    # --------------------------------------------------
    #
    # invoke():
    #
    # query embedding banayega
    # similarity search karega
    # top chunks return karega

    retrieved_docs = retriever.invoke(query)


    print("\n========== RETRIEVED RESULTS ==========\n")


    for index, doc in enumerate(retrieved_docs):

        print(f"\n----- RESULT {index} -----\n")

        print(doc.page_content)


    # --------------------------------------------------
    # ACCUMULATE RESULTS
    # --------------------------------------------------
    #
    # Saare retrieved docs combine kar rahe hain.
    #
    # Fusion systems generally:
    # multiple retrieval outputs merge karte hain.

    all_retrieved_docs.extend(retrieved_docs)


# ======================================================
# DEDUPLICATION
# ======================================================

# IMPORTANT PROBLEM:
#
# Same chunk multiple queries se retrieve ho sakta hai.
#
# Isliye deduplication required hota hai.
#
# Simple strategy:
#
# chunk text ko unique key treat karenge.

unique_docs = {}


for doc in all_retrieved_docs:

    # page_content ko dictionary key bana rahe hain
    #
    # Agar same text dubara aaya,
    # overwrite ho jayega.
    #
    # Final result:
    # unique chunks only.

    unique_docs[doc.page_content] = doc


# Final deduplicated list

fused_results = list(unique_docs.values())


# ======================================================
# FINAL FUSED RESULTS
# ======================================================

print("\n================ FINAL FUSED RESULTS ================\n")

print(f"Total unique chunks: {len(fused_results)}")


for index, doc in enumerate(fused_results):

    print(f"\n========== FUSED CHUNK {index} ==========\n")

    print(doc.page_content)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne single user query li.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

Us query ki multiple semantic variations banayi.

Example:

"How does RAG work?"
↓
"Explain retrieval pipeline"
↓
"How are embeddings used?"

--------------------------------------------------------
STEP 3
--------------------------------------------------------

Har query variation separately retrieve hui.

IMPORTANT:

Different wording
↓
Different embeddings
↓
Different retrieval paths

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Saare retrieval results combine hue.

--------------------------------------------------------
STEP 5
--------------------------------------------------------

Duplicate chunks remove hue.

Final result:

fused_results

========================================================
MOST IMPORTANT INSIGHT
========================================================

Fusion ka goal:
accuracy improve karna nahi.

PRIMARY goal:
RECALL improve karna.

Meaning:

"relevant information miss kam ho"

========================================================
WHY FUSION WORKS
========================================================

Semantic search imperfect hota hai.

Ek wording:
kuch chunks retrieve karegi.

Dusri wording:
different chunks retrieve karegi.

Fusion:
multiple semantic perspectives combine karta hai.

========================================================
IMPORTANT REAL-WORLD INSIGHT
========================================================

Advanced production RAG systems often spend:
MORE engineering effort on retrieval
than on generation.

Because:

Better retrieval
↓
Better grounding
↓
Better answers

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
↓
FUSION

NEXT FILE:

prompts.py

Waha hum seekhenge:

retrieved chunks ko
LLM prompt me inject kaise kiya jata hai.

Yahi actual:
"Retrieval-Augmented Generation"

moment hoga.

========================================================
"""