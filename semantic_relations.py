from wiki_ru_wordnet import WikiWordnet

wikiwn = WikiWordnet()

def get_synonyms(sense):
    return [w.lemma() for w in sense.get_words()]

def get_hypernyms(sense):
    result = []
    for h_sense in wikiwn.get_hypernyms(sense):
        for word in h_sense.get_words():
            result.append(word.lemma())
    return result

def get_hyponyms(sense):
    result = []
    for h_sense in wikiwn.get_hyponyms(sense):
        for word in h_sense.get_words():
            result.append(word.lemma())
    return result

def get_all_relations(sense):
    return {
        'synonyms': get_synonyms(sense),
        'hypernyms': get_hypernyms(sense),
        'hyponyms': get_hyponyms(sense),
    }
