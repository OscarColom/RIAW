import os
from json import JSONEncoder
import pandas as pd

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
import nltk
from flask import Flask, render_template, session
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus, tweet_to_doc_map
from myapp.search.objects import Document, StatsDocument
from myapp.search.search_engine import SearchEngine
from myapp.search.algorithms import create_inverted_index_tfidf, build_terms

import uuid
import time
from datetime import datetime
from user_agents import parse

# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***

# instantiate the Flask application
app = Flask(__name__)

# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
# print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.

#file_path = path + "/tweets-data-who.json"
file_path = path + "/json_test.json"



# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path)
#print(corpus)
print("loaded corpus. first elem:", list(corpus.values())[0])


inv_index, tf, df, idf = create_inverted_index_tfidf(corpus, tweet_to_doc_map)


# Home URL "/"
@app.route('/')
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2021 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    # Save the last search query to the session
    session['last_search_query'] = search_query

    # Generate a unique visitor ID for the session if it doesn't exist
    if 'visitor_id' not in session:
        session['visitor_id'] = str(uuid.uuid4())  # Generate a unique UUID as visitor ID

    # Store the search query in the session to track search history
    if 'search_queries' not in session:
        session['search_queries'] = []
    
    # Add the current search query to the search history
    session['search_queries'].append(search_query)

    # Limit search query history to the last 10 queries (for memory efficiency)
    session['search_queries'] = session['search_queries'][-10:]

    # Collect additional data
    query_length = len(search_query)  # Total number of characters
    num_terms = len(search_query.split())  # Number of terms in the search query
    term_order = search_query.split()  # Terms in the order entered

    # Create a timestamp for the search query
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Now save the query using the AnalyticsData instance
    search_id = analytics_data.save_query_terms(
        search_query, num_terms, query_length, term_order, session['visitor_id']
    )

    # Perform the search (keep the rest of your search logic as-is)
    results = search_engine.search(search_query, search_id, corpus, inv_index, tf, df, idf)

    # Calculate the number of results found
    found_count = len(results)
    session['last_found_count'] = found_count

    # Render results with the search query and other stats
    return render_template(
        'results.html', 
        results_list=results, 
        page_title="Results", 
        found_counter=found_count, 
        search_query=search_query
    )


@app.route('/results', methods=['GET'])
def results():
    search_query = session.get('last_search_query')  # Retrieve the query from the session
    if not search_query:
        return "Search query is missing", 400  # Handle empty queries

    results = search_engine.search(search_query, None, corpus, inv_index, tf, df, idf)
    found_count = len(results)

    return render_template(
        'results.html',
        results_list=results,
        page_title="Results",
        found_counter=found_count,
        search_query=search_query
    )


@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = request.args["id"]
    clicked_doc_id = int(clicked_doc_id)
    
    #p1 = int(request.args["search_id"])  # transform to Integer
    #p2 = int(request.args["param2"])  # transform to Integer
    #print("click in id={}".format(clicked_doc_id))

    if clicked_doc_id in corpus:
        document = corpus[clicked_doc_id]  # Obtener el documento usando su ID
        print(f"Document found: {document}")
    else:
        return "Document not found", 404


    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

    #return render_template('doc_details.html')
    return render_template(
        'doc_details.html',
        document=document,  # Pasar el documento completo a la plantilla
        click_count=analytics_data.fact_clicks[clicked_doc_id]  # También pasamos la estadística de clics
    )




@app.route('/stats')
def stats():
    # Mocking total requests (to be replaced with a real tracking method)
    total_requests = 1000

    # HTTP Sessions Data
    unique_visitors = len(session.keys())

    # Gather Visitor Data
    user_agent_string = request.headers.get('User-Agent')
    
    # Parse the user-agent string using user_agents library
    user_agent = parse(user_agent_string)
    
    # Extract browser, OS, and device
    browser = user_agent.browser.family
    os = user_agent.os.family
    device = "Mobile" if user_agent.is_mobile else "Desktop"
    time_of_day = datetime.now().strftime('%H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')

    visitor_data = {
        'browser': browser,
        'os': os,
        'device': device,
        'time_of_day': time_of_day,
        'date': date
    }

    docs = []
    total_clicks = 0
    unique_visitors = len(session.keys())  # Assuming session stores unique users

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]
        total_clicks += count
        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count)
        docs.append(doc)

    # Calculate the average clicks per document
    average_clicks_per_doc = total_clicks / len(docs) if docs else 0



    return render_template(
        'stats.html',
        page_title="Quick Stats",
        total_requests=total_requests,
        total_clicks=total_clicks,
        unique_visitors=unique_visitors,
        average_clicks_per_doc=average_clicks_per_doc,
        recent_searches=[query['query'] for query in analytics_data.queries[-11:]],
        clicks_data=docs,
        analytics_queries=analytics_data.queries,
        visitor_data=visitor_data,
    )









@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    for doc in visited_docs: print(doc)
    return render_template('dashboard.html', visited_docs=visited_docs)


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)
