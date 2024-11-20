import nltk
nltk.download('stopwords')

from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
import numpy as np
import collections
from numpy import linalg as la
import json
import string
import re
import pandas as pd
from collections import Counter
import math


def build_terms(line):

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

    line = re.sub(r"http\S+|www\S+|https\S+", '', line, flags=re.MULTILINE)  #remove URLs

    line = line.lower() #lowercase

    tokens = line.split() #tokenize


    processed_tokens = []
    for token in tokens:

        if token.startswith('#'):
            processed_tokens.append(token) #keep hasthags exactly as they are
        else:
            token = token.translate(str.maketrans('', '', string.punctuation)) #remove punctuations

            if token and token not in stop_words: #eliminate the stopwords
                stemmed_token = stemmer.stem(token) #stemming
                processed_tokens.append(stemmed_token)

    return processed_tokens

def create_inverted_index_tfidf(tweets, tweet_to_doc_map):
    """
    Implement the inverted index and compute tf, df, and idf.

    Returns:
    index - the inverted index containing terms as keys and the corresponding list of documents these keys appear in (and the positions) as values.
    tf - normalized term frequency for each term in each document
    df - number of documents each term appears in
    idf - inverse document frequency of each term
    """

    index = defaultdict(list)
    tf = defaultdict(list)
    df = defaultdict(int)
    idf = defaultdict(float)

    num_documents = len(set(tweet_to_doc_map.values()))

    for tweet_id, document in tweets.items():

        doc_id = tweet_to_doc_map.get(tweet_id)

        if doc_id is not None:

            tweet_content = document.description
            terms = build_terms(tweet_content)
            current_doc_index = defaultdict(list)

            # Create current document index
            for position, term in enumerate(terms):
                current_doc_index[term].append(position)

            # Normalize term frequencies
            norm = math.sqrt(sum(len(postings) ** 2 for postings in current_doc_index.values()))

            for term, postings in current_doc_index.items():
                tf_val = np.round(len(postings) / norm, 4)
                if doc_id not in index[term]:  # Avoid duplicates
                    index[term].append((doc_id, postings))
                    tf[term].append(tf_val)
                    df[term] += 1

    # Compute IDF
    for term in df:
        idf[term] = np.round(np.log(float(num_documents) / df[term]), 4)

    return index, tf, df, idf




def rank_documents(query, docs, index, idf, tf):
    """
    Perform the ranking of the results of a search based on the tf-idf weights.

    Returns:
    List of ranked documents along with their scores
    """

    # Process query into terms and initialize vectors
    query_terms = build_terms(query)
    query_vector = [0] * len(query_terms)
    doc_vectors = defaultdict(lambda: [0] * len(query_terms))

    # Count term frequency in query and normalize
    query_terms_count = Counter(query_terms)
    query_norm = la.norm([query_terms_count[term] for term in query_terms])

    # Build the query vector and each document vector
    for term_idx, term in enumerate(query_terms):
        if term in index:
            # Calculate the normalized term frequency for the query
            query_vector[term_idx] = (query_terms_count[term] / query_norm) * idf.get(term, 0)

            # Update document vectors with term frequencies and normalize
            for doc_idx, (doc, postings) in enumerate(index[term]):
                if doc in docs:
                    tf_norm = tf[term][doc_idx]  # Already normalized in tf calculation
                    doc_vectors[doc][term_idx] = tf_norm * idf[term]

    # Calculate normalized scores for each document
    doc_scores = []
    for doc, doc_vec in doc_vectors.items():
        doc_norm = la.norm(doc_vec)
        if doc_norm != 0:
            normalized_score = np.dot(doc_vec, query_vector) / doc_norm  # Normalize with document norm
            doc_scores.append([normalized_score, doc])

    # Sort documents by their relevance scores in descending order
    doc_scores.sort(reverse=True, key=lambda x: x[0])

    # Return ordered documents and their scores
    return [doc for _, doc in doc_scores], doc_scores




def search_in_corpus(query):
    # 1. create create_tfidf_index

    # 2. apply ranking
    return ""
