# search_elastic_word2vec.py
# Εκτέλεση επεκταμένων ερωτημάτων word2vec στην Elasticsearch και αποθήκευση αποτελεσμάτων

from elasticsearch import Elasticsearch
from expand_queries import expanded_queries  # από το προηγούμενο αρχείο

es = Elasticsearch("http://localhost:9200")  # ή ανάλογα με τη ρύθμισή σου

INDEX_NAME = "ir2025_index"
TOP_K = 100
METHOD_NAME = "word2vec_phase3"

results = []

for qid, query_text in expanded_queries:
    response = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "match": {
                    "text_content": {
                        "query": query_text
                    }
                }
            }
        },
        size=TOP_K
    )

    for rank, hit in enumerate(response["hits"]["hits"]):
        doc_id = hit["_id"]
        score = hit["_score"]
        results.append(f"{qid} Q0 {doc_id} {rank+1} {score} {METHOD_NAME}")

# Αποθήκευση αποτελεσμάτων
with open("results.txt", "w", encoding="utf-8") as f:
    for line in results:
        f.write(line + "\n")

print("✅ Αποθηκεύτηκαν τα αποτελέσματα στο results.txt")
