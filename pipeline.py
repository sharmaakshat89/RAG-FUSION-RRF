"""
========================================================
pipeline.py
========================================================

YE FILE RAG PIPELINE KA SEVENTH LAYER HAI:
ORCHESTRATION LAYER

Abhi tak humne har layer separately build ki thi:

- ingestion
- chunking
- embeddings
- retrieval
- fusion
- prompting

Ab next important step:

--------------------------------------------------------
QUESTION:
--------------------------------------------------------

Real systems me ye saari layers
ek saath kaise kaam karti hain?

Yahi orchestration layer ka kaam hai.

========================================================
MENTAL MODEL
========================================================

User Query
↓
Retrieval
↓
Fusion
↓
Prompt Construction
↓
LLM
↓
Final Answer

========================================================
VERY IMPORTANT INSIGHT
========================================================

Production AI systems usually:
"many small specialized layers"

se milkar bante hain.

Pipeline orchestration ka kaam:
in layers ko connect karna hota hai.

========================================================
IMPORTANT ARCHITECTURAL INSIGHT
========================================================

Ab tak humne intentionally:
- separate files
- reusable outputs
- modular imports
- isolated abstractions

build kiye.

Ab:
pipeline.py

sabko ek connected intelligence flow me transform karega.

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Previous layers ke reusable artifacts import kar rahe hain.
#
# IMPORTANT:
#
# Ye modularity ka actual benefit hai.
#
# Har layer independently understandable bhi hai
# aur reusable bhi.

from retrieval import retriever

from langchain_openai import ChatOpenAI

import os


# ======================================================
# OPENAI API KEY
# ======================================================

# LLM generation ke liye API key required hai.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ======================================================
# INITIALIZE LLM
# ======================================================

# IMPORTANT:
#
# Embedding model aur chat model different hote hain.
#
# Embedding model:
# semantic vectors banata hai
#
# Chat model:
# final text answer generate karta hai

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini"
)


# ======================================================
# QUERY VARIATION GENERATOR
# ======================================================

# Fusion layer me hum manually multiple queries likh rahe the.
#
# Ab orchestration layer me
# us logic ko reusable function bana rahe hain.
#
# IMPORTANT:
#
# Ye real engineering progression hai:
#
# prototype code
# ↓
# reusable functions

def generate_query_variations(user_query):

    """
    User query ko multiple semantic perspectives me
    convert karta hai.
    """

    return [

        user_query,

        f"Explain: {user_query}",

        f"Describe the concept of {user_query}",

        f"How does {user_query} work?",

        f"Technical explanation of {user_query}"
    ]


# ======================================================
# MULTI QUERY RETRIEVAL
# ======================================================

# Ye function:
#
# - multiple query variations banayega
# - retrieval run karega
# - results combine karega
# - duplicates remove karega

def retrieve_with_fusion(user_query):

    # --------------------------------------------------
    # QUERY GENERATION
    # --------------------------------------------------

    queries = generate_query_variations(user_query)


    # All retrieved chunks yaha accumulate honge

    all_docs = []


    # --------------------------------------------------
    # MULTIPLE RETRIEVAL PASSES
    # --------------------------------------------------

    for query in queries:

        print(f"\n================ QUERY =================\n")

        print(query)


        # Semantic retrieval

        retrieved_docs = retriever.invoke(query)


        # Results accumulate karo

        all_docs.extend(retrieved_docs)


    # --------------------------------------------------
    # DEDUPLICATION
    # --------------------------------------------------
    #
    # Same chunk multiple queries se aa sakta hai.

    unique_docs = {}


    for doc in all_docs:

        unique_docs[doc.page_content] = doc


    # Final deduplicated retrieval results

    fused_docs = list(unique_docs.values())


    return fused_docs


# ======================================================
# CONTEXT BUILDER
# ======================================================

# Retrieved chunks ko:
#
# LLM-readable prompt context
#
# me convert karega.

def build_context(retrieved_docs):

    context_parts = []


    for index, doc in enumerate(retrieved_docs):

        context_parts.append(

            f"""
            ==============================
            CONTEXT CHUNK {index}
            ==============================

            {doc.page_content}
            """
        )


    return "\n".join(context_parts)


# ======================================================
# PROMPT BUILDER
# ======================================================

# Final RAG prompt construct karega.

def build_prompt(user_query, context_text):

    prompt = f"""

    You are a helpful AI assistant.

    Answer the question ONLY using the provided context.

    If answer is not available in context,
    clearly say that the information was not found.

    ==================================================
    CONTEXT
    ==================================================

    {context_text}

    ==================================================
    USER QUESTION
    ==================================================

    {user_query}

    ==================================================
    ANSWER
    ==================================================

    """

    return prompt


# ======================================================
# MAIN RAG PIPELINE
# ======================================================

# YEH ACTUAL COMPLETE RAG ORCHESTRATION HAI.
#
# Is function me:
#
# query
# ↓
# retrieval
# ↓
# fusion
# ↓
# prompt construction
# ↓
# LLM generation
#
# complete end-to-end flow run hoga.

def run_rag_pipeline(user_query):

    print("\n==================================================")
    print("STARTING RAG PIPELINE")
    print("==================================================\n")


    # --------------------------------------------------
    # STEP 1: RETRIEVAL + FUSION
    # --------------------------------------------------

    print("\n========== STEP 1: RETRIEVAL ==========\n")

    retrieved_docs = retrieve_with_fusion(user_query)


    print("\n========== RETRIEVED DOC COUNT ==========\n")

    print(len(retrieved_docs))


    # --------------------------------------------------
    # STEP 2: CONTEXT BUILDING
    # --------------------------------------------------

    print("\n========== STEP 2: CONTEXT BUILDING ==========\n")

    context_text = build_context(retrieved_docs)


    # --------------------------------------------------
    # STEP 3: PROMPT CONSTRUCTION
    # --------------------------------------------------

    print("\n========== STEP 3: PROMPT CONSTRUCTION ==========\n")

    final_prompt = build_prompt(
        user_query,
        context_text
    )


    print(final_prompt)


    # --------------------------------------------------
    # STEP 4: LLM GENERATION
    # --------------------------------------------------

    print("\n========== STEP 4: LLM GENERATION ==========\n")

    response = llm.invoke(final_prompt)


    # --------------------------------------------------
    # STEP 5: FINAL ANSWER
    # --------------------------------------------------

    print("\n========== FINAL ANSWER ==========\n")

    print(response.content)


    return response.content


# ======================================================
# TEST THE COMPLETE PIPELINE
# ======================================================

# Real-world systems me ye:
#
# - chatbot input
# - API endpoint
# - frontend request
#
# se trigger hota hai.

test_question = "Explain how the RAG pipeline works"


final_answer = run_rag_pipeline(test_question)


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

User query aayi.

Example:

"Explain how the RAG pipeline works"

--------------------------------------------------------
STEP 2
--------------------------------------------------------

Query variations generate hue.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

Multiple semantic retrieval passes hue.

--------------------------------------------------------
STEP 4
--------------------------------------------------------

Retrieved chunks fuse hue.

--------------------------------------------------------
STEP 5
--------------------------------------------------------

Chunks:
LLM-readable context me convert hue.

--------------------------------------------------------
STEP 6
--------------------------------------------------------

Final RAG prompt build hua.

User question
+
Retrieved context
=
Grounded prompt

--------------------------------------------------------
STEP 7
--------------------------------------------------------

Prompt LLM ko diya gaya.

--------------------------------------------------------
STEP 8
--------------------------------------------------------

LLM ne:
retrieved context ke basis par
final grounded answer generate kiya.

========================================================
MOST IMPORTANT SYSTEMS INSIGHT
========================================================

RAG ek single model nahi hota.

RAG:
multiple specialized layers ka orchestrated system hota hai.

========================================================
WHY MODULARITY MATTERS
========================================================

Agar sab kuch ek giant file me hota:
- debugging difficult
- scaling difficult
- testing difficult
- mental model weak

Current architecture:
- layered
- reusable
- inspectable
- debuggable

========================================================
VERY IMPORTANT ENGINEERING INSIGHT
========================================================

Most production AI engineering actually:
"data flow orchestration"

hoti hai.

Not:
"just calling GPT"

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
↓
PROMPT AUGMENTATION
↓
LLM GENERATION

NEXT FILE:

api.py

Waha hum:
entire RAG pipeline ko
FastAPI endpoint me expose karenge.

Meaning:

external apps
↓
HTTP requests
↓
RAG pipeline
↓
AI responses

========================================================
"""