from elasticsearch import Elasticsearch
import json

# Σύνδεση με το τοπικό Elasticsearch instance
es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "trec-covid"

# Αν υπάρχει ήδη index με το ίδιο όνομα, τον διαγράφουμε
if es.indices.exists(index=INDEX_NAME):
    print(f"Deleting existing index '{INDEX_NAME}'...")
    es.indices.delete(index=INDEX_NAME)

# Δημιουργία του index με ρύθμιση analyzer και mappings
print(f"Creating index '{INDEX_NAME}'...")
es.indices.create(index=INDEX_NAME, body={
    "settings": {
        "number_of_shards": 1,
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "abstract": {"type": "text"}
        }
    }
})

# Εισαγωγή εγγράφων από το corpus.jsonl
print("Indexing documents from corpus.jsonl...")
with open("trec-covid/corpus.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        doc = json.loads(line)
        es.index(index=INDEX_NAME, id=doc["id"], body={
            "id": doc["id"],
            "title": doc.get("title", ""),
            "abstract": doc.get("abstract", "")
        })
        if i % 1000 == 0:
            print(f"{i} documents indexed...")

print("All documents indexed successfully.")
