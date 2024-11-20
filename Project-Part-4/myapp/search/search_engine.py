import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import create_inverted_index_tfidf, rank_documents
from myapp.search.load_corpus import tweet_to_doc_map, doc_to_tweet_map


def build_demo_results(corpus: dict, search_id):
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    res = []
    size = len(corpus)
    ll = list(corpus.values())
    for index in range(random.randint(0, 40)):
        item: Document = ll[random.randint(0, size)]
        res.append(ResultItem(item.id, item.title, item.description, item.doc_date,
                              "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id), random.random()))

    # for index, item in enumerate(corpus['Id']):
    #     # DF columns: 'Id' 'Tweet' 'Username' 'Date' 'Hashtags' 'Likes' 'Retweets' 'Url' 'Language'
    #     res.append(DocumentInfo(item.Id, item.Tweet, item.Tweet, item.Date,
    #                             "doc_details?id={}&search_id={}&param2=2".format(item.Id, search_id), random.random()))

    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


# class SearchEngine:
#     """educational search engine"""

#     def search(self, search_query, search_id, corpus):
#         print("Search query:", search_query)

#         results = []
#         ##### your code here #####
#         results = build_demo_results(corpus, search_id)  # replace with call to search algorithm

#         # results = search_in_corpus(search_query)
#         ##### your code here #####

#         return results


# class SearchEngine:
#     """educational search engine"""

#     def search(self, search_query, search_id, corpus):
#         print("Search query:", search_query)

#         # Obtener el índice invertido y las métricas (tf, df, idf)
#         index, tf, df, idf = create_inverted_index_tfidf(corpus, tweet_to_doc_map)

#         # Obtener la lista de documentos
#         docs = list(set(doc for postings in index.values() for doc, _ in postings))

#         # Llamar a la función de ranking para obtener los documentos ordenados
#         results, scores = rank_documents(search_query, docs, index, idf, tf)

#         # Crear los ResultItems para cada documento y su puntuación
#         ranked_results = []
#         for result in results[:20]:  # Limitar a los primeros 20 resultados
#             item = corpus[result]  # Obtener el documento del corpus
#             ranked_results.append(ResultItem(item.id, item.title, item.description, item.doc_date,
#                                               "doc_details?id={}&search_id={}".format(item.id, search_id), scores[result][0]))

#         return ranked_results

class SearchEngine:
    """Educational search engine"""

    def search(self, search_query, search_id, corpus):
        print("Search query:", search_query)

        # Crear el índice invertido y las métricas (tf, df, idf)
        index, tf, df, idf = create_inverted_index_tfidf(corpus, tweet_to_doc_map)

        # Obtener la lista de documentos
        docs = list(set(doc for postings in index.values() for doc, _ in postings))

        # Llamar a la función de ranking para obtener los documentos ordenados
        results, scores = rank_documents(search_query, docs, index, idf, tf)

        # Traducir los doc_id a tweet_id usando el diccionario doc_to_tweet_map
        tweet_ids = [doc_to_tweet_map[result] for result in results if result in doc_to_tweet_map]

        # Crear los ResultItems para los top-20 documentos
        ranked_results = []
        for i, tweet_id in enumerate(tweet_ids[:20]):  # Usar índice explícito para mantener alineación
            if tweet_id in corpus:
                item = corpus[tweet_id]  # Acceder al documento del corpus usando tweet_id
                ranked_results.append(ResultItem(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    doc_date=item.doc_date,
                    url=f"doc_details?id={item.id}&search_id={search_id}",
                    ranking=scores[i]  # Usar el índice `i` para obtener el score correcto
                ))

        return ranked_results
