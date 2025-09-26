#Πρέπει να προσαρμοστούν τα αρχεια εισόδου και εξόδου ανάλογα με το σενάριο.
import re
from collections import defaultdict

def convert_wordnet_pl_to_synonyms_txt(pl_file_path, txt_file_path):
    synsets = defaultdict(list)
    
    
    line_regex = re.compile(r"s\((\d+),\d+,'([^']+)',[nvar],\d+,\d+\)\.")

    try:
        with open(pl_file_path, 'r', encoding='utf-8') as f_in:
            for line in f_in:
                match = line_regex.match(line)
                if match:
                    synset_id = match.group(1)
                    word = match.group(2).lower() # Μετατροπή σε πεζά
                    if ' ' not in word and '_' not in word: # Απλοποίηση: αγνοούμε λέξεις με κενά ή underscores
                        if word not in synsets[synset_id]: # Αποφυγή διπλότυπων μέσα στο ίδιο synset
                             synsets[synset_id].append(word)
    except FileNotFoundError:
        print(f"Error: Prolog file not found at {pl_file_path}")
        return
    except Exception as e:
        print(f"An error occurred during reading: {e}")
        return

    try:
        with open(txt_file_path, 'w', encoding='utf-8') as f_out:
            for synset_id, words in synsets.items():
                if len(words) > 1: 
                    f_out.write(",".join(words) + "\n")
        print(f"Successfully converted {pl_file_path} to {txt_file_path}")
    except Exception as e:
        print(f"An error occurred during writing: {e}")

if __name__ == '__main__':
    
    input_pl_file = 'WordNetFiles/wn_s_verbs.pl'  # Αρχείο Prolog με τα συνώνυμα
    
   
    output_txt_file = 'wordnet_verbs_synonyms_converted.txt'

    convert_wordnet_pl_to_synonyms_txt(input_pl_file, output_txt_file)
