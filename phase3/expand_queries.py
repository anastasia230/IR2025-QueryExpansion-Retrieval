# expand_queries.py
# Επέκταση ερωτημάτων IR2025 με λέξεις από word2vec μοντέλο

import json
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec

# Φόρτωση εκπαιδευμένου μοντέλου
model = Word2Vec.load("word2vec.model")

# Φόρτωση ερωτημάτων
expanded_queries = []

with open("queries.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        q = json.loads(line)
        qid = q["query_id"]
        text = q["query"]
        tokens = word_tokenize(text.lower())
        expanded = tokens.copy()

        for token in tokens:
            if token in model.wv:
                similar = model.wv.most_similar(token, topn=3)
                expanded += [w for w, _ in similar]

        expanded_text = " ".join(expanded)
        expanded_queries.append((qid, expanded_text))

# Επιστροφή επέκτασης (για επόμενη χρήση)
for qid, query in expanded_queries:
    print(f"{qid} -> {query}")
