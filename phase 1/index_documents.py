import json
from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", verify_certs=False)

INDEX_NAME = "trec-covid"

print("Elasticsearch info:", es.info())

# Αν υπάρχει ήδη index με το ίδιο όνομα, τον διαγράφουμε
if es.indices.exists(index=INDEX_NAME):
    print(f"Deleting existing index '{INDEX_NAME}'...")
    es.indices.delete(index=INDEX_NAME)

# Δημιουργία του index
print(f"Creating index '{INDEX_NAME}'...")
es.indices.create(index=INDEX_NAME, body={
    "settings": {
        "number_of_shards": 1
    },
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "abstract": {"type": "text"},
            "text": {"type": "text"}  # <-- Ενιαίο πεδίο για ευκολία στην αναζήτηση
        }
    }
})

#  Εισαγωγή εγγράφων
with open("corpus.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        doc = json.loads(line)

        if "_id" not in doc:
            print(f"Skipping doc at line {i} (no '_id')")
            continue  # Παράλειψη αν δεν έχει _id

        combined_text = f"{doc.get('title', '')} {doc.get('text', '')}"
        es.index(index=INDEX_NAME, id=doc["_id"], body={
            "id": doc["_id"],
            "title": doc.get("title", ""),
            "abstract": doc.get("text", ""),  # <-- από το `text` του αρχείου
            "text": combined_text
        })

        if i % 1000 == 0:
            print(f"{i} documents processed...")

print("All documents indexed successfully.")
