import pandas as pd
import json
import os


from myapp.core.utils import load_json_file
from myapp.search.objects import Document

_corpus = {}



base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
docs_path_map = os.path.join(base_dir, 'tweet_document_ids_map.csv')
df = pd.read_csv(docs_path_map)

doc_to_tweet_map = dict(zip(df['docId'], df['id']))  # mapa de docId a tweetId
tweet_to_doc_map = dict(zip(df['id'], df['docId']))  # mapa de tweetId a docId



def load_corpus(path) -> [Document]:
    """
    Load file and transform to dictionary with each document as an object for easier treatment when needed for displaying
     in results, stats, etc.
    :param path:
    :return:
    """
    df = _load_corpus_as_dataframe(path)
    df.apply(_row_to_doc_dict, axis=1)
    return _corpus


def _load_corpus_as_dataframe(path):
    """
    Load documents corpus from file in 'path'
    :return:
    """
        #json_data = load_json_file(path)
    with open(path) as fp:
        lines = fp.readlines()
    lines = [l.strip().replace(' +', ' ') for l in lines]
    tweets = [json.loads(line.strip()) for line in lines]
    json_data = tweets


    tweets_df = _load_tweets_as_dataframe(json_data)
    _clean_hashtags_and_urls(tweets_df)
    # Rename columns to obtain: Tweet | Username | Date | Hashtags | Likes | Retweets | Url | Language
    corpus = tweets_df.rename(
        columns={
        "id": "Id", 
        "content": "Tweet",  # Cambié full_text a content
        "username": "Username", 
        "created": "Date", 
        "likeCount": "Likes",  # Cambié favorite_count a likeCount
        "retweetCount": "Retweets", 
        "lang": "Language"
    })

    # select only interesting columns
    filter_columns = ["Id", "Tweet", "Username", "Date", "Likes", "Retweets", "Url", "Language"]
    corpus = corpus[filter_columns]
    return corpus


def _load_tweets_as_dataframe(json_data):

    #print("JSON data preview:", json_data[:5])
    data = pd.DataFrame(json_data)
    # parse entities as new columns
    #data = pd.concat([data.drop(['entities'], axis=1), data['entities'].apply(pd.Series)], axis=1)
    # parse user data as new columns and rename some columns to prevent duplicate column names
    data = pd.concat([data.drop(['user'], axis=1), data['user'].apply(pd.Series).rename(
        columns={"created_at": "user_created_at", "id": "user_id", "id_str": "user_id_str", "lang": "user_lang"})],
                     axis=1)
    return data


def _build_tags(row):
    tags = []
    # for ht in row["hashtags"]:
    #     tags.append(ht["text"])
    for ht in row:
        tags.append(ht["text"])
    return tags


def _build_url(row):
    url = ""
    try:
        url = row["entities"]["url"]["urls"][0]["url"]  # tweet URL
    except:
        try:
            url = row["retweeted_status"]["extended_tweet"]["entities"]["media"][0]["url"]  # Retweeted
        except:
            url = ""
    return url


def _clean_hashtags_and_urls(df):
    print(df.columns)
    #df["Hashtags"] = df["hashtags"].apply(_build_tags)
    df["Url"] = df.apply(lambda row: _build_url(row), axis=1)
    # df["Url"] = "TODO: get url from json"
    #df.drop(columns=["entities"], axis=1, inplace=True)


def load_tweets_as_dataframe2(json_data):
    """Load json into a dataframe

    Parameters:
    path (string): the file path

    Returns:
    DataFrame: a Panda DataFrame containing the tweet content in columns
    """
    # Load the JSON as a Dictionary
    tweets_dictionary = json_data.items()
    # Load the Dictionary into a DataFrame.
    dataframe = pd.DataFrame(tweets_dictionary)
    # remove first column that just has indices as strings: '0', '1', etc.
    dataframe.drop(dataframe.columns[0], axis=1, inplace=True)
    return dataframe


def load_tweets_as_dataframe3(json_data):
    """Load json data into a dataframe

    Parameters:
    json_data (string): the json object

    Returns:
    DataFrame: a Panda DataFrame containing the tweet content in columns
    """

    # Load the JSON object into a DataFrame.
    dataframe = pd.DataFrame(json_data).transpose()

    # select only interesting columns
    filter_columns = ["id", "full_text", "created_at", "entities", "retweet_count", "favorite_count", "lang"]
    dataframe = dataframe[filter_columns]
    return dataframe


def _row_to_doc_dict(row: pd.Series):
    _corpus[row['Id']] = Document(row['Id'], row['Tweet'][0:100], row['Tweet'], row['Date'], row['Likes'],
                                  row['Retweets'],
                                  row['Url'])
