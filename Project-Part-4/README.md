# Project-Part-4.   Search Engine with Web Analytics 

## Before Starting the Web App
Before starting the web app, it is important that the folder includes two files: a JSON file containing the tweets, which should be named farmers-protest-tweets; the other file is a CSV file containing the mapping of documents with the tweet_id and should be named tweet_document_ids_map. Both files can be found here:https://drive.google.com/drive/folders/1UEizot0aYHSPVGko7EIZ1kH00O11Gyr2?usp=drive_link.
It is also important to note that the web app may take some time to run initially, as the first thing it does when starting is calculate the inverted index. Once the initial search page is loaded, it should work normally. If this is not the case, you can run it using a smaller corpus.
Please note that for the Web Analytics section, data is stored in memory.
## Starting the Web App

```bash
python -V
# Make sure you are using Python 3
# Before running the code, make sure you are in the folder where the web_app.py file and data files are located.
python web_app.py

```
## Starting Web App
The web app's functionality is quite simple. The first page you see is the main page with a search bar. Enter the desired query and press "Search". The next page will show a list of the 20 most relevant documents related to that query. To access the document details, simply click on the document title or "Doc Details", which will open the document details. On this page, you can go back to view the other results ("Go Back"), return to the homepage ("Go Back 2 pages"), or view some statistics ("Stats"). To return to the homepage from "Stats", click on the UPF logo.
The analytics dashboard part is not done.


