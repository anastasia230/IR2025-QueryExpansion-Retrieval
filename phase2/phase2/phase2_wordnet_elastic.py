#Πρέπει να προσαρμοστούν τα αρχεια εισόδου και εξόδου ανάλογα με το σενάριο.
import json
import os
from elasticsearch import Elasticsearch, exceptions
from tqdm import tqdm


# --- Configuration ---
# Elasticsearch connection details
ELASTIC_HOST = 'http://localhost:9200'

# Index and file paths
INDEX_NAME = 'phase2_wordnet_verbs_graph' 
COLLECTION_FILE_PATH = 'corpus.jsonl' 
QUERIES_PATH = 'queries.jsonl'         
RESULTS_FILE_PATH = 'results.txt' 

# Path to the synonym file *inside the Elasticsearch container's config directory*
# This path is relative to the Elasticsearch config directory, e.g., /usr/share/elasticsearch/config/
SYNONYM_FILE_PATH_IN_CONTAINER = "analysis/wordnet_verbs_synonyms_converted.txt"

# --- Elasticsearch Client ---
def get_es_client():
    """Initializes and returns an Elasticsearch client."""
    try:
        client = Elasticsearch(ELASTIC_HOST, request_timeout=30, max_retries=10, retry_on_timeout=True)
        if not client.ping():
            raise ValueError("Connection to Elasticsearch failed!")
        print("Successfully connected to Elasticsearch.")
        return client
    except Exception as e:
        print(f"Error connecting to Elasticsearch: {e}")
        return None

# --- Index Management ---
def create_index_with_synonym_graph_analyzer(es_client):
    """
    Creates an Elasticsearch index with a custom analyzer using a synonym graph token filter.
    """
    if es_client.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists. Deleting it.")
        es_client.indices.delete(index=INDEX_NAME)

    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "wordnet_analyzer": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "wordnet_synonyms_filter"  
                        ]
                    }
                },
                "filter": {
                    "wordnet_synonyms_filter": {
                        "type": "synonym_graph",
                        "synonyms_path": SYNONYM_FILE_PATH_IN_CONTAINER,
                        "format": "solr"  
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "text_content": {
                    "type": "text",
                    "analyzer": "wordnet_analyzer",  
                    "search_analyzer": "wordnet_analyzer"  
                }
            }
        }
    }

    try:
        es_client.indices.create(index=INDEX_NAME, body=index_settings)
        print(f"Index '{INDEX_NAME}' created successfully with 'wordnet_analyzer'.")
    except exceptions.RequestError as e:
        print(f"Error creating index: {e.info['error']['root_cause']}")
        if 'caused_by' in e.info['error']:
            print(f"Caused by: {e.info['error']['caused_by']}")
    except Exception as e:
        print(f"An unexpected error occurred during index creation: {e}")

def index_ir2025_collection(es_client):
   
    print(f"Starting to index documents from '{COLLECTION_FILE_PATH}' into '{INDEX_NAME}'...")
    actions = []
    doc_count = 0

    if not os.path.exists(COLLECTION_FILE_PATH):
        print(f"ERROR: Collection file '{COLLECTION_FILE_PATH}' not found.")
        return

    with open(COLLECTION_FILE_PATH, 'r', encoding='utf-8') as f:
        for line in tqdm(f, desc="Indexing documents"):
            try:
                doc = json.loads(line.strip())
                doc_id = doc.get('_id')
                title = doc.get('title', '')       # Get title, default to empty string if not present
                abstract = doc.get('abstract', '') # Get abstract, default to empty string if not present

                if not doc_id:
                   
                    continue

               
                text_content_to_index = f"{title} {abstract}".strip()

                action = {
                    "_index": INDEX_NAME,
                    "_id": doc_id, # Use 'doc_id' from the collection as the Elasticsearch document ID
                    "_source": {
                        "doc_id": doc_id, # Store doc_id explicitly in the source as well
                        "text_content": text_content_to_index
                    }
                }
                actions.append(action)
                doc_count += 1

                if len(actions) >= 500:
                    from elasticsearch.helpers import bulk
                    bulk(es_client, actions)
                    actions = [] # Reset actions list
            except json.JSONDecodeError:
                print(f"Skipping line due to JSON decode error: {line.strip()}")
            except Exception as e:
                print(f"Error processing document: {doc_id if 'doc_id' in locals() else 'Unknown ID'}, Error: {e}")


    if actions: # Index any remaining actions
        from elasticsearch.helpers import bulk
        bulk(es_client, actions)

    es_client.indices.refresh(index=INDEX_NAME) # Refresh index to make documents searchable
    print(f"Successfully indexed {doc_count} documents into '{INDEX_NAME}'.")


# --- Querying and Results ---
def run_ir2025_queries_and_collect_results(es_client, run_id="phase2_wordnet_verbs_syns"):
    """
    Runs queries from the specified queries file (JSONL format) against the Elasticsearch index
    and saves results in trec_eval format.
    Assumes queries file is in .jsonl format with '_id' and 'text' fields.
    """
    print(f"Running queries from '{QUERIES_PATH}'...")
    if not os.path.exists(QUERIES_PATH):
        print(f"ERROR: Queries file '{QUERIES_PATH}' not found.")
        return

    results = []
    with open(QUERIES_PATH, 'r', encoding='utf-8') as f_queries:
        for line_number, line in enumerate(tqdm(f_queries, desc="Processing queries"), 1):
            line = line.strip()
            if not line:
                continue

            try:
                # Ανάλυση της γραμμής JSON
                query_data = json.loads(line)
                query_id = query_data.get('_id')
                query_text = query_data.get('text')

                if not query_id or not query_text:
                    print(f"Skipping line {line_number} due to missing '_id' or 'text': {line}")
                    continue

            except json.JSONDecodeError:
                print(f"Skipping line {line_number} due to JSON decode error: {line}")
                continue
            except Exception as e:
                print(f"Skipping line {line_number} due to unexpected error ('{e}'): {line}")
                continue


            query_body = {
                "query": {
                    "match": {
                        "text_content": query_text
                    }
                },
                "_source": ["doc_id"],
                "size": 100 
            }

            try:
                response = es_client.search(index=INDEX_NAME, body=query_body)
                rank = 1
                for hit in response['hits']['hits']:
                    doc_id_retrieved = hit['_source'].get('doc_id', hit['_id'])
                    score = hit['_score']
                    results.append(f"{query_id}\tQ0\t{doc_id_retrieved}\t{rank}\t{score}\t{run_id}\n")
                    rank += 1
            except exceptions.ElasticsearchException as e:
                print(f"Error searching for query ID '{query_id}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing query ID '{query_id}': {e}")

    # Write results to file

    with open(RESULTS_FILE_PATH, 'w', encoding='utf-8') as f_results:
        for result_line in results:
            f_results.write(result_line)
    print(f"Results saved to '{RESULTS_FILE_PATH}'.")
    print(f"You can now run trec_eval: trec_eval <qrels_file> {RESULTS_FILE_PATH}") 



# --- Main Execution ---
if __name__ == '__main__':
    es = get_es_client()
    if es:
        # 1. Create index with custom analyzer
        create_index_with_synonym_graph_analyzer(es)

        # 2. Index documents from the collection
        index_ir2025_collection(es)

        # 3. Run queries and collect results
        run_ir2025_queries_and_collect_results(es, run_id="phase2_wordnet_verbs_syns") # Example run_id

    else:
        print("Could not connect to Elasticsearch. Exiting.")