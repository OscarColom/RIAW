import random

from myapp.search.objects import ResultItem, Document
from myapp.search.algorithms import  rank_documents
from myapp.search.load_corpus import  doc_to_tweet_map


class SearchEngine:
    """Educational search engine"""

    def search(self, search_query, search_id, corpus, index, tf, df, idf):
        print("Search query:", search_query)

        
        docs = list(set(doc for postings in index.values() for doc, _ in postings))


        results, scores = rank_documents(search_query, docs, index, idf, tf)


        tweet_ids = [doc_to_tweet_map[result] for result in results if result in doc_to_tweet_map]

        ranked_results = []
        for i, tweet_id in enumerate(tweet_ids[:20]):  
            if tweet_id in corpus:
                item = corpus[tweet_id]  
                ranked_results.append(ResultItem(
                    id=item.id,
                    title=item.title,
                    description=item.description,
                    doc_date=item.doc_date,
                    url=f"doc_details?id={item.id}&search_id={search_id}",
                    ranking=scores[i]  
                ))

        return ranked_results
