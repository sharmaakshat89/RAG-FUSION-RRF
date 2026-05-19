RAG FUSION

query vector is very crucial
simil search gives satisfactory results in most cases
but we are dependent on the user to ask the right query. retrieval quality depends on the keywords user inputs in his query
USER DEPENDENCY HIGH

1st step : Rephrasing ther user query : like multi query retriever
query to llm to rephrase
rephrased queries to retriever to do simil search in vector db

2nd step : reranking these retrievals instead of deduping ( like in multi query)
we use algo called RRF for reranking 


RECIPROCAL RANK FUSION  <---->  RRF
 rank of retrieved query, one that consistently appears in all rephrased query retrievals.
 a document that is not consistently appearing in all the results is given lower score.

 CONSISTENCY OF APPEARANCE IN RESULTS OF REPHRASED QUERIES RETRIEVAL

RRF score : summation of 1/(rank + kc)
kc is a constant , used as 60 in most cases( 60 gives most optimum results)
suppose a doc x comes in 3 retrieved resp (with rank 3 in first query resp , rank 1 in 2nd , no appearance in 3rd )
so its rrf score will be ( assuming kc = 60)

doc x = 1/(3+60) + 1/(1+60) +  0 (as it did not appear in result of 3rd rephrased query)

similar scoring for : doc y & doc z

now all these reranked based on RRF Score
then top K docs fetched 




