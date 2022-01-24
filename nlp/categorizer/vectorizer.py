from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from categorizer.tokenizer import spacy_tokenizer

bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))
