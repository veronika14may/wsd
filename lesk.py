from wiki_ru_wordnet import WikiWordnet
from preprocess import preprocess, clean_definition, simple_tokenize, stop_words, morph

wikiwn = WikiWordnet()

def get_sense_text(sense):
    text_parts = []
    for word in sense.get_words():
        raw = word.definition()
        if raw:
            text_parts.append(clean_definition(raw))
    return ' '.join(text_parts)

def build_signature(sense):
    text = get_sense_text(sense)
    return preprocess(text)

def get_sense_label(sense):
    words = [w.lemma() for w in sense.get_words()]
    return ', '.join(words)

def clean_target(word):
    w = word.lower()
    lemma = morph.parse(w)[0].normal_form
    return {w, lemma}

def get_context_words(word, sentence):
    tokens = simple_tokenize(sentence.lower())
    target_forms = clean_target(word)
    
    result = []
    for tok in tokens:
        if not tok.isalpha() or len(tok) < 2:
            continue
        if tok in stop_words:
            continue
        lemma = morph.parse(tok)[0].normal_form
        if lemma in stop_words:
            continue
        if lemma in target_forms or tok in target_forms:
            continue
        result.append(lemma)
    
    return result

def classical_lesk(word, sentence):
    lemma = morph.parse(word.lower())[0].normal_form
    senses = wikiwn.get_synsets(lemma)
    if len(senses) == 0:
        return None
    
    neighbors = get_context_words(word, sentence)
    
    best_sense = senses[0]
    best_score = 0
    
    for sense in senses:
        target_sig = build_signature(sense)
        total_score = 0
        
        for neighbor in neighbors:
            neighbor_senses = wikiwn.get_synsets(neighbor)
            if len(neighbor_senses) == 0:
                continue
            best_neighbor_overlap = 0
            for n_sense in neighbor_senses:
                n_sig = build_signature(n_sense)
                overlap = len(target_sig & n_sig)
                if overlap > best_neighbor_overlap:
                    best_neighbor_overlap = overlap
            total_score += best_neighbor_overlap
        
        if total_score > best_score:
            best_score = total_score
            best_sense = sense
    
    return best_sense, best_score

def show_all_senses(word):
    lemma = morph.parse(word.lower())[0].normal_form
    senses = wikiwn.get_synsets(lemma)
    print(f"Всего значений у слова '{word}' (лемма '{lemma}'): {len(senses)}")
    for i, s in enumerate(senses):
        label = get_sense_label(s)
        definition = get_sense_text(s)
        if len(definition) > 150:
            definition = definition[:150] + "..."
        print(f"  {i+1}) [{label}] — {definition}")