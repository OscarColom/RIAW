# -*- coding: utf-8 -*-
"""PROJECT_ part_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qudpIhnq0XVpCU0AiS6p6K9THn6gPUNy

# **IRWA_LAB_PART1**

# **0. LOADINGS**
"""

from google.colab import drive
drive.mount('/content/drive', force_remount=True)

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

docs_path = '/content/drive/MyDrive/RIAW/IRWA_data_2024/data/farmers-protest-tweets.json'
with open(docs_path) as fp:
    lines = fp.readlines()
lines = [l.strip().replace(' +', ' ') for l in lines]

tweets = [json.loads(line.strip()) for line in lines]

print("Total number of tweets : {}".format(len(tweets)))

"""# **1. TEXT PROCESSING**

1) As a first step, you must pre-process the documents by

● Removing stop words

● Tokenization

● Removing punctuation marks

● Stemming

● and... anything else you think it's needed (bonus point)

### **TRANSLATION HINDI TO ENGLISH  (NOT REQUIRED TO EXECUTE)**
"""

!pip install googletrans==3.1.0a0

#as a 1st step, we translate hindi tweets to english, as they are heavily important in this dataset we do not want to get rid of them
#we consider them as english tweets after translation to make our life easier, adding a tag to each tweet of the language of the tweet originally

from googletrans import Translator


translator = Translator()

def translate_tweet_add_lang_tag(tweet_text):

    detected_lang = translator.detect(tweet_text).lang #detecting the language

    if detected_lang != 'en':
        translated_text = translator.translate(tweet_text, dest='en').text
    else:
        translated_text = tweet_text  #we don't do anything if it was english

    return translated_text, detected_lang

progress = 0
translated_tweets = tweets

for tweet in translated_tweets:

    if progress % 10000 == 0:
        print(f"processed {progress} tweets")

    translated_text, detected_language = translate_tweet_add_lang_tag(tweet['content'])

    tweet['content'] = translated_text #updating the content into english
    tweet['language'] = detected_language #adding the column with the language of the tweet

    progress += 1

tweets[69]['content']

translated_tweets[69]['content']

#Save translated tweets
import json

with open('/content/drive/MyDrive/RIAW/IRWA_data_2024/data/translated_tweets.json', 'w', encoding='utf-8') as f:
    json.dump(translated_tweets, f, ensure_ascii=False, indent=4)

"""### **TO OPEN THE FILE WITH THE TRANSLATED TWEETS**"""

with open('/content/drive/MyDrive/RIAW/IRWA_data_2024/data/translated_tweets.json', 'r', encoding='utf-8') as f:
    translated_tweets = json.load(f)

translated_tweets[3]

print(tweets[69]['content']) #example before translation

print(translated_tweets[69]['content']) #example after translation
print(translated_tweets[69]['language'])

"""### **FUNCTION TO PRE-PROCESS THE DOCUMENTS AND PRE-PROCESSING OF ORIGINAL AND TRANSLATED**"""

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

terms_of_each_tweet = []

for tweet in tweets:
    terms_of_each_tweet.append(build_terms(tweet['content']))

#example
print(terms_of_each_tweet[1])

#Cretae terms for the translated tweets
terms_of_each_translated_tweet = []

for tweet in translated_tweets:
    terms_of_each_translated_tweet.append(build_terms(tweet['content']))

"""## **Bidirectional Mapping for the tweet’s Ids with the document ids for evaluation**"""

docs_path_map = '/content/drive/MyDrive/RIAW/IRWA_data_2024/data/tweet_document_ids_map.csv'

df = pd.read_csv(docs_path_map)


doc_to_tweet_map = dict(zip(df['docId'], df['id']))  #map doc to tweet id

tweet_to_doc_map = dict(zip(df['id'], df['docId']))  #map tweet_id to doc


doc_id = 'doc_0'
tweet_id = doc_to_tweet_map.get(doc_id)
print(f"doc_id {doc_id} have id {tweet_id}")


doc_id_10 = tweet_to_doc_map.get(1364505314586951680)
print(f"doc_id {doc_id_10} have id {1364505314586951680}")

"""# **2. RETURN Tweet | Date | Hashtags| Likes | Retweets | Url**

FOR ORIGINAL TWEETS
"""

import re

filtered_tweets = []
i = 0

for tweet in tweets:

    content = tweet['content']
    date = tweet['date']
    likes = tweet['likeCount']
    retweets = tweet['retweetCount']
    url = tweet['url']
    id = tweet['id']

    #creating new column for the hasthags + need to find them
    hashtags = re.findall(r'#\w+', content)

    filtered_tweet = {
        'Content': content,
        'Date': date,
        'Hashtags': hashtags,
        'Likes': likes,
        'Retweets': retweets,
        'Url': url,
        'id': id,
        'clean terms': terms_of_each_tweet[i]
    }

    filtered_tweets.append(filtered_tweet)

    i += 1

filtered_tweets[0]

"""FOR TRANSALTED TWEETS"""

import re

filtered_translated_tweets = []
i = 0

# Iterar sobre los translated_tweets y terms_of_each_translated_tweet
for tweet in translated_tweets:

    content = tweet['content']
    date = tweet['date']
    likes = tweet['likeCount']
    retweets = tweet['retweetCount']
    url = tweet['url']
    id = tweet['id']

    # Crear nueva columna para los hashtags (encontrar hashtags en el tweet traducido)
    hashtags = re.findall(r'#\w+', content)

    # Crear el tweet filtrado con los términos del tweet traducido
    filtered_tweet = {
        'Content': content,
        'Date': date,
        'Hashtags': hashtags,
        'Likes': likes,
        'Retweets': retweets,
        'Url': url,
        'id': id,
        'clean terms': terms_of_each_translated_tweet[i]  # Asignar términos traducidos
    }

    filtered_translated_tweets.append(filtered_tweet)

    i += 1  # Incrementar el índice para recorrer terms_of_each_translated_tweet

filtered_translated_tweets[69]  #See example with a tweed that originaly was in hindi

"""# **3. EXPLORATORY DATA ANALYSIS**

* word counting distribution
* average sentence length
* vocabulary size
* ranking of tweets most retweeted
* word clouds for the most frequent words
* entity recognition -> nombres propios/instituciones/palabras que van juntas siempre

**GENERAL STATISTICS FOR ORIGINAL TWEETS**
"""

import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


all_terms = [term for tweet_terms in terms_of_each_tweet for term in tweet_terms] #list with all terms
word_counts = Counter(all_terms)

most_common_words = word_counts.most_common(10)  #top10

def count_words(text):
    return len(text.split())

total_words = sum(word_counts.values())
unique_words = len(word_counts)
avg_terms_per_tweet = total_words / len(terms_of_each_tweet)
word_counts = [count_words(tweet['Content']) for tweet in filtered_tweets]
average_sentence_length = sum(word_counts) / len(word_counts)

print("Total number of tweets : {}".format(len(tweets)))
print(f"Total Words: {total_words}")
print(f"Vocabulary Size: {unique_words}")
print(f"Average Clean Terms Per Tweet: {avg_terms_per_tweet:.2f}")
print(f"Average Sentence Length (in words): {average_sentence_length:.2f}")

"""**WORD DISTRIBUTION**"""

most_common_words

"""**As we can see some of the most common words in the tweets are in hindi so we are going to do some data analysis of the transaled tweet to undestand better the data**"""

all_translated_terms = [term for tweet_terms in terms_of_each_translated_tweet for term in tweet_terms]  # lista con todos los términos
word_counts_translated = Counter(all_translated_terms)

most_common_translated_words = word_counts_translated.most_common(10)  # top 10

def count_words(text):
    return len(text.split())

total_translated_words = sum(word_counts_translated.values())
unique_translated_words = len(word_counts_translated)
avg_terms_per_translated_tweet = total_translated_words / len(terms_of_each_translated_tweet)


translated_word_counts = [count_words(tweet['Content']) for tweet in filtered_translated_tweets]
average_translated_sentence_length = sum(translated_word_counts) / len(translated_word_counts)

print("Total number of translated tweets: {}".format(len(translated_tweets)))
print(f"Total Translated Words: {total_translated_words}")
print(f"Vocabulary Size (Translated): {unique_translated_words}")
print(f"Average Clean Terms Per Translated Tweet: {avg_terms_per_translated_tweet:.2f}")
print(f"Average Sentence Length (in words) for Translated Tweets: {average_translated_sentence_length:.2f}")

most_common_translated_words

"""**HISTOGRAM FOR TERMS OF ORIGINAL TWEETS**"""

import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


all_terms = [term for tweet_terms in terms_of_each_tweet for term in tweet_terms] #list with all terms
word_counts = Counter(all_terms)

most_common_words = word_counts.most_common(10)  #top10


words, counts = zip(*most_common_words)

#plot histogram
plt.figure(figsize=(10, 6))
plt.bar(words, counts)
plt.xticks(rotation=45, ha='right')
plt.title('Top10 Common Terms')
plt.ylabel('frequency')
plt.xlabel('terms')
plt.tight_layout()
plt.show()

"""**HISTOGRAM FOR TERMS OF TRANSLATED TWEETS**"""

all_translated_terms = [term for tweet_terms in terms_of_each_translated_tweet for term in tweet_terms]  # lista con todos los términos
translated_word_counts = Counter(all_translated_terms)

most_common_translated_words = translated_word_counts.most_common(10)  # top 10

# Separar palabras y cuentas
translated_words, translated_counts = zip(*most_common_translated_words)

# Plotear histograma
plt.figure(figsize=(10, 6))
plt.bar(translated_words, translated_counts)
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Common Terms in Translated Tweets')
plt.ylabel('Frequency')
plt.xlabel('Terms')
plt.tight_layout()
plt.show()

"""**MOST RETWEETED**"""

most_retweeted_tweets = sorted(filtered_tweets, key=lambda x: x['Retweets'], reverse=True) #sorting with most to less retweeted

top_n = 10

print(f"Top {top_n} Most Retweeted Tweets:")
for i, tweet in enumerate(most_retweeted_tweets[:top_n], 1):
    print(f"\nTOP {i}:")
    print(f"Retweets: {tweet['Retweets']}")
    print(f"Content: {tweet['Content']}")
    print(f"URL: {tweet['Url']}")

"""**HASTHAGS DISTRIBUTION**"""

all_hashtags = []

for tweet in filtered_tweets:
    all_hashtags.extend( tweet['Hashtags'])

hashtag_counts = Counter(all_hashtags) #counting frequency
most_common_hashtags = hashtag_counts.most_common(10) #top10

print("Top 10 Hashtags + occurrences\n")
for hashtag in most_common_hashtags:
    print(hashtag)

"""**WORDCLOUD WITH TOP 50 MOST USED HASHTAGS**"""

from wordcloud import WordCloud

hashtag_dict = dict(hashtag_counts)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(hashtag_dict)


plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Hashtags")
plt.show()

"""**WORD CLOUD FOR TOP 50 NON-HASHTAG CLEAN TERMS**

*FOR ORIGINAL TWEETS*
"""

all_terms = []

for tweet in filtered_tweets:
    terms = tweet['clean terms']
    terms_without_hastag = [term for term in terms if not term.startswith('#')]
    all_terms.extend(terms_without_hastag)

term_counts = Counter(all_terms) #counting frequency
most_common_termss = term_counts.most_common(50) #top50 for wordcloud

print("Top 10 non-hashtag clean terms + occurrences\n")
i = 0
for term in most_common_termss:
    if i <= 10:
        print(term)
        i += 1
    else:
        break

term_dict = dict(most_common_termss)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(term_dict)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Words")
plt.show()

"""*NOW FOR ALL THE TWEETS TRANSLATED*"""

all_translated_terms = []

for tweet in filtered_translated_tweets:
    terms = tweet['clean terms']  # Asegúrate de que esta clave contenga los términos de los tweets traducidos
    terms_without_hashtag = [term for term in terms if not term.startswith('#')]  # Filtrar los hashtags
    all_translated_terms.extend(terms_without_hashtag)  # Agregar términos a la lista

translated_term_counts = Counter(all_translated_terms)

most_common_translated_terms = translated_term_counts.most_common(50)

print("Top 10 non-hashtag clean terms + occurrences\n")
for i, term in enumerate(most_common_translated_terms):
    if i < 10:  # Cambiado de <= a < para evitar la última iteración
        print(term)

translated_term_dict = dict(most_common_translated_terms)

wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(translated_term_dict)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Most Common Words in Translated Tweets")
plt.show()

"""**ENTITY RECOGNITION**"""

#We install spacy, to have the needed rules for entity recognition
!pip install spacy
!python -m spacy download en_core_web_sm

import spacy

# Load the pre-trained English model from spaCy
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):

    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]  # TO get the entities and their labels
    return entities

# Add recognized entities to each tweet
for tweet in filtered_tweets:
    content = tweet['Content']
    entities = extract_entities(content)
    tweet['Entities'] = entities

# Print the first few tweets with their recognized entities
for tweet in filtered_tweets[:5]:
    print(f"Tweet: {tweet['Content']}")
    print(f"Entities: {tweet['Entities']}")
    print('-' * 80)

from collections import Counter

# We create an entity counter to count the frequency of each entity label
entity_counter = Counter()

for tweet in filtered_tweets:
    for entity in tweet['Entities']:
        entity_counter[entity[1]] += 1

# Print of the top 10 most common entity types and their counts
print("Top 10 Entity Types:")
for entity, count in entity_counter.most_common(10):
    print(f"{entity}: {count}")