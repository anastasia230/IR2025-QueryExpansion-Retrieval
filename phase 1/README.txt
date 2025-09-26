===========================
README - IR2025 Project
===========================

Αριθμός Μητρώου: 3210008  
Όνομα: Αναστασία Ανδρομίδα  
Μοντέλο Ανάκτησης: Vector Space Model (TF-IDF)  
Μηχανή Αναζήτησης: Elasticsearch  
Εργαλείο Αξιολόγησης: trec_eval

---------------------------
Βήματα Εκτέλεσης:
---------------------------

1. Εκκίνηση Elasticsearch
--------------------------
Βεβαιωθείτε ότι ο Elasticsearch server τρέχει στη διεύθυνση:
http://localhost:9200

Μπορείτε να ξεκινήσετε τον Elasticsearch μέσω:
> bin\elasticsearch.bat  (σε Windows)

2. Δημιουργία Ευρετηρίου & Εισαγωγή Κειμένων
---------------------------------------------
Εκτελέστε το παρακάτω αρχείο:
> python index_documents.py

Αυτό θα:
- Δημιουργήσει index στο Elasticsearch με όνομα "trec-covid"
- Εισάγει τα κείμενα από το corpus.jsonl (δεν περιλαμβάνεται στο zip)

3. Εκτέλεση Ερωτημάτων & Δημιουργία Αρχείων .run
-------------------------------------------------
Εκτελέστε:
> python search_documents.py

Το script αυτό δημιουργεί τα αρχεία:
- results_k20.run
- results_k30.run
- results_k50.run

με τα top-k σχετικά έγγραφα ανά ερώτημα.

4. Αξιολόγηση με trec_eval
---------------------------
Εκτελέστε:
> trec_eval qrels.test results.test

(το αρχείο results.test είναι μια από τις εκδόσεις αποτελεσμάτων)

Θα εμφανιστούν τα μέτρα:
- MAP
- avgPrecision@5,10,15,20
- P@k

Τα αποτελέσματα καταγράφηκαν στο PDF της αναφοράς.

---------------------------
Περιεχόμενα ZIP
---------------------------

- index_documents.py
- search_documents.py
- qrels.test
- results.test
- results_k20.run
- results_k30.run
- results_k50.run
- ergasia sap.pdf
- README.txt

Σημείωση: Το corpus.jsonl **δεν περιλαμβάνεται** λόγω μεγέθους, όπως ζητήθηκε.



