import re
import pymorphy3
from nltk.corpus import stopwords

morph = pymorphy3.MorphAnalyzer()

def simple_tokenize(text):
    return re.findall(r'[а-яёА-ЯЁa-zA-Z]+', text)

def load_stopwords():
    return set(stopwords.words('russian'))
 
stop_words = load_stopwords()

def clean_definition(text):
    if '~ru~' in text:
        parts = text.split('~ru~')
        text = parts[-1]
    
    while '{{' in text and '}}' in text:
        text = re.sub(r'\{\{[^{}]*\}\}', ' ', text)

    text = re.sub(r'\[\[([^\[\]|]*?)\]\]', r'\1', text)
    text = re.sub(r'\[\[[^\[\]|]*?\|([^\[\]]*?)\]\]', r'\1', text)
    text = re.sub(r'~\d+~\d+', '', text)
    text = re.sub(r'<!--.*?-->', '', text)
    text = re.sub(r'[#~|]+', ' ', text)
    text = re.sub(r'^[\s,;.]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def preprocess(text):
    text = text.lower()
    tokens = simple_tokenize(text)
    
    clean_tokens = []
    for token in tokens:
        if not token.isalpha():
            continue
        if len(token) < 2:
            continue
        if token in stop_words:
            continue

        lemma = morph.parse(token)[0].normal_form
        if lemma in stop_words:
            continue
        clean_tokens.append(lemma)

    return set(clean_tokens)
