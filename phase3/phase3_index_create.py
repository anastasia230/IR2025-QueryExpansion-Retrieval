# phase3_index_create.py

import json
from elasticsearch import Elasticsearch, helpers

# 1. Σύνδεση με Elasticsearch
es = Elasticsearch("http://localhost:9200")

# 2. Όνομα index
index_name = "ir2025_index"

# 3. Αν υπάρχει ήδη το index, το διαγράφουμε
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 4. Ορίζουμε αναλυτή και mapping
index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "english_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop"],
                    "stopwords": ["_english_"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "doc_id": {"type": "keyword"},
            "text": {
                "type": "text",
                "analyzer": "english_analyzer"
            }
        }
    }
}

# 5. Δημιουργία index με catch σφάλματος
try:
    es.indices.create(index=index_name, body=index_settings)
except Exception as e:
    print("\u26a0\ufe0f Σφάλμα κατά τη δημιουργία του index:")
    print(e)
    exit()

# 6. Φόρτωση εγγραφών
with open("corpus.jsonl", "r", encoding="utf-8") as f:
    documents = [json.loads(line) for line in f]

# 7. Bulk insert
actions = [
    {
        "_index": index_name,
        "_id": doc["doc_id"],
        "_source": doc
    }
    for doc in documents
]

helpers.bulk(es, actions)

print(f"✅ Επιτυχής δημιουργία του index '{index_name}' με {len(actions)} έγγραφα.")
