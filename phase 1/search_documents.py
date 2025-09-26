import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "trec-covid"
TOP_K = [20, 30, 50]

with open("queries.jsonl", "r", encoding="utf-8") as f:

    queries = [json.loads(line) for line in f]

for k in TOP_K:
    run_filename = f"results_k{k}.run"
    with open(run_filename, "w", encoding="utf-8") as out:
        for q in queries:
            query_id = q["_id"]
            query_text = q["metadata"]["query"]

            res = es.search(index=INDEX_NAME, size=k, query={
                "match": {
                    "abstract": {
                        "query": query_text
                    }
                }
            })

            for rank, hit in enumerate(res["hits"]["hits"], start=1):
                doc_id = hit["_id"]
                score = hit["_score"]
                out.write(f"{query_id} Q0 {doc_id} {rank} {score} STANDARD\n")

    print(f"saved results in {run_filename}")
