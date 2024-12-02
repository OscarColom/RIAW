import random
import json
from datetime import datetime
from myapp.search.algorithms import build_terms



class AnalyticsData:
    """
    An in-memory persistence object.
    This class will track and store analytics for search queries and document clicks.
    """
    def __init__(self):
        # Initialize fact_clicks as an instance attribute (dictionary)
        self.fact_clicks = {}

        # Other statistics can also be initialized here
        self.queries = []  # To store query data
        self.fact_two = {}
        self.fact_three = {}

    def save_query_terms(self, terms: str, num_terms: int, query_length: int, term_order: list, visitor_id: str) -> int:
        """
        Save a search query along with its associated stats (num_terms, query_length, etc.).
        Generates a unique search ID and stores the query data.
        """
        search_id = random.randint(0, 100000)
        query_data = {
            'search_id': search_id,
            'query': terms,
            'num_words': num_terms,
            'query_length': query_length,
            'terms': build_terms(terms),
            'num_terms': len(build_terms(terms)),
            'term_order': term_order,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'visitor_id': visitor_id
        }
        self.queries.append(query_data)
        return search_id
    

    def record_click_(self, doc_id: str, description: str):
        """
        Record a click for a document.
        If the document exists in fact_clicks, increment the counter. Otherwise, initialize it.
        """
        if doc_id in self.fact_clicks:
            self.fact_clicks[doc_id].counter += 1
        else:
            self.fact_clicks[doc_id] = ClickedDoc(doc_id, description, 1)

    def record_click(self, doc_id: str, description: str, rank=0, query_related=None):
        """
        Record a click for a document, along with ranking and related query data.
        """
        if doc_id in self.fact_clicks:
            self.fact_clicks[doc_id].counter += 1
        else:
            self.fact_clicks[doc_id] = ClickedDoc(doc_id, description, 1, rank, query_related)




    def get_all_clicks(self):
        """
        Retrieve all clicked document data.
        """
        return [doc.to_json() for doc in self.fact_clicks.values()]

    def get_query_by_id(self, search_id: int):
        """
        Retrieve a specific query by its search ID.
        """
        return next((query for query in self.queries if query['search_id'] == search_id), None)




class ClickedDoc_:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
    
class ClickedDoc:
    def __init__(self, doc_id, description, counter, rank=0, query_related=None, dwell_time=0):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter
        self.rank = rank
        self.query_related = query_related
        self.dwell_time = dwell_time

    def to_json(self):
        return self.__dict__

    def __str__(self):
        return json.dumps(self)

