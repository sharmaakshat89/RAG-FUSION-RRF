"""
========================================================
prompts.py
========================================================

YE FILE RAG PIPELINE KA SIXTH LAYER HAI:
PROMPT AUGMENTATION LAYER

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

Ab ek VERY IMPORTANT QUESTION:

--------------------------------------------------------
QUESTION:
--------------------------------------------------------

Retrieved chunks ka actual use kaise hota hai?

Kya LLM automatically vector DB access karta hai?

❌ Nahi.

LLM directly vector DB nahi padhta.

Instead:

Retrieved context manually prompt me inject kiya jata hai.

ISI KO bolte hain:

"Retrieval-Augmented Generation"

========================================================
MOST IMPORTANT RAG INSIGHT
========================================================

RAG ka actual secret:

LLM ko retrieved knowledge
prompt ke andar feed ki jati hai.

Meaning:

User Question
+
Retrieved Context
↓
LLM

========================================================
MENTAL MODEL
========================================================

User Query
↓
Retriever
↓
Relevant Chunks
↓
Prompt Context Injection
↓
LLM
↓
Grounded Answer

========================================================
VERY IMPORTANT CONCEPT
========================================================

Without retrieval:

LLM answers from training memory.

With retrieval:

LLM answers using supplied external context.

Yahi hallucination reduction ka foundation hai.

========================================================
"""


# ======================================================
# IMPORTS
# ======================================================

# Previous layer se fused retrieval results import kar rahe hain.
#
# IMPORTANT:
#
# Ye chunks already:
# - semantically relevant hain
# - deduplicated hain
# - retrieval layer se filtered hain

from fusion import fused_results


# ======================================================
# USER QUESTION
# ======================================================

# Real-world systems me ye:
#
# - chatbot message
# - API request
# - frontend textbox
#
# se aata hai.

user_question = "Explain how this RAG pipeline works"


# ======================================================
# BUILD CONTEXT STRING
# ======================================================

# LLM directly Document objects understand nahi karta.
#
# Isliye retrieved chunks ko:
#
# structured text context
#
# me convert karna padta hai.
#
# Ye VERY IMPORTANT STEP hai.
#
# Yahi actual:
# "context injection"
#
# moment hai.

context_parts = []


# ======================================================
# CONVERT CHUNKS INTO CONTEXT
# ======================================================

# Har retrieved chunk ko
# readable context format me convert karenge.
#
# IMPORTANT:
#
# Chunk separators useful hote hain.
#
# Kyun?
#
# Taaki LLM ko samajh aaye:
# ye different retrieved passages hain.

for index, doc in enumerate(fused_results):

    context_parts.append(

        f"""
        ==============================
        CONTEXT CHUNK {index}
        ==============================

        {doc.page_content}
        """
    )


# ======================================================
# FINAL CONTEXT
# ======================================================

# Saare chunks combine ho kar
# ek giant context block ban jayenge.

context_text = "\n".join(context_parts)


# ======================================================
# BUILD FINAL PROMPT
# ======================================================

# YE RAG PIPELINE KA MOST IMPORTANT CONCEPTUAL MOMENT HAI.
#
# Yaha:
#
# retrieved knowledge
# +
# user question
#
# combine ho rahe hain.
#
# LLM ko:
#
# "external grounded context"
#
# diya ja raha hai.
#
# IMPORTANT:
#
# Prompt engineering ka goal:
#
# - LLM ko guide karna
# - hallucination reduce karna
# - retrieved context use karwana

final_prompt = f"""

You are a helpful AI assistant.

Answer the user question ONLY using the provided context.

If the answer is not present in the context,
say:
"I could not find the answer in the retrieved documents."

==================================================
RETRIEVED CONTEXT
==================================================

{context_text}

==================================================
USER QUESTION
==================================================

{user_question}

==================================================
ANSWER
==================================================

"""


# ======================================================
# DEBUGGING / INSPECTION
# ======================================================

# Prompt inspection extremely important hota hai.
#
# Most RAG bugs actually:
# prompt construction issues hote hain.
#
# Verify:
#
# - context properly injected hua?
# - formatting readable hai?
# - chunk boundaries clear hain?
# - user question included hai?

print("\n================ FINAL PROMPT ================\n")

print(final_prompt)


# ======================================================
# OPTIONAL: PROMPT SIZE INSPECTION
# ======================================================

# Real-world RAG systems me:
# token limits bahut important hote hain.
#
# Giant context:
# - expensive ho sakta hai
# - truncation cause kar sakta hai
# - latency increase kar sakta hai

print("\n================ PROMPT CHARACTER COUNT ================\n")

print(len(final_prompt))


"""
========================================================
WHAT ACTUALLY HAPPENED?
========================================================

STEP-BY-STEP mentally dekho.

--------------------------------------------------------
STEP 1
--------------------------------------------------------

Humne:
fused_results

retrieve kiye.

Ye semantically relevant chunks the.

--------------------------------------------------------
STEP 2
--------------------------------------------------------

Chunks ko raw Document objects se
readable text context me convert kiya.

--------------------------------------------------------
STEP 3
--------------------------------------------------------

Saare chunks combine hue:

CONTEXT BLOCK
ban gaya.

--------------------------------------------------------
STEP 4
--------------------------------------------------------

User question +
Retrieved context
=
Final RAG prompt

========================================================
MOST IMPORTANT RAG INSIGHT
========================================================

LLM ko:
"knowledge upload"
nahi hoti dynamically.

Instead:

Every query ke time:
relevant context prompt me inject hota hai.

Yahi RAG hai.

========================================================
WITHOUT RAG
========================================================

User Question
↓
LLM memory

Possible issue:
hallucinations

========================================================
WITH RAG
========================================================

User Question
↓
Retriever
↓
External context
↓
LLM grounded answer

========================================================
VERY IMPORTANT INSIGHT
========================================================

RAG systems fundamentally:

"Context engineering systems"

hote hain.

Retrieval ka goal:
correct context lana.

Prompting ka goal:
LLM ko correct context use karwana.

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

NEXT FILE:

pipeline.py

Waha hum:
entire RAG flow
ek orchestrated procedural pipeline me connect karenge.

========================================================
"""