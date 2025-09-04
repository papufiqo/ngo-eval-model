import nltk
from collections import Counter
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_themes(feedback_texts, top_n=5):
    stop_words = set(stopwords.words('english'))
    all_words = []
    for text in feedback_texts:
        words = word_tokenize(re.sub(r'[^a-zA-Z\s]', '', text.lower()))
        words = [w for w in words if w not in stop_words and len(w) > 3]
        all_words.extend(words)
    freq = Counter(all_words)
    return freq.most_common(top_n)
