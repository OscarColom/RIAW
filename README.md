# IRWA PROJECT

## PART 1

- **Description -->** In the 1st part of the project, we pre-process some tweets from a farmer protest in 2021 and perform a data analysis of them.
- **Data Used -->** As mentioned in the report, we worked with Hindi tweets translated to English, therefore we create a json file with all the tweets translated to English.
This file must be downloaded as we use it in our notebook. Instructions for it are given below.
- **Usage -->** The python notebook "project__part_1.py" was done in Google Colab, therefore it is recommended to download it and execute it using Colab. We divided
  the notebook into 4 main blocks.
  
### Block 0 (Loading) 
It's just meant to be executed to do all the imports we need and load data. 

### Block 1 (Text Processing) 
Here we start translating from tweets to translated_tweets, but it's very time-consuming, so we recommend not running the cells in "TRANSLATION HINDI TO ENGLISH
(NOT REQUIRED TO EXECUTE)" and go directly to the next section "TO OPEN THE FILE WITH THE TRANSLATED TWEETS", where one should load the translated_tweet.json, you can download this file here: https://drive.google.com/file/d/1IvhXbLlRGY_M5ExfVrNq3dfcXPegmoCw/view?usp=drive_link and uploaded to Google Drive (change paths as needed). With this load, we can then execute all the remaining cells in the block where we do 
the processing from the content of the tweets to clean processed terms. We also map the tweets with their doc ids, which will be of relevance for the next project part.
If needed the rest  of the data can be downloaded here: https://drive.google.com/drive/folders/1UEizot0aYHSPVGko7EIZ1kH00O11Gyr2?usp=drive_link 

### Block 2 (Return) 
In this block, we only create filtered_tweets and filtered_translated_tweets to retrieve only information of relevance, which is for each tweet its Tweet | Date | Hashtags| 
Likes | Retweets | Url | id | clean terms. All cells must be run in order.

### Block 3 (Data Analysis) 
In this last block, we perform a data analysis separately for tweets and translated_tweets, creating charts and lists of the most retweeted tweets, most used words or hashtags, wordclouds, and entity recognition. This last section requires loading the Spacy model for English, and it's a little time-consuming. All cells must be run in order.


## PART 2

- **Description -->** In the 2nd part of the project, we create TF-IDF indices for our documents (tweets) and then use some test queries to evaluate the performance of our system with some metrics.
- **Data Used -->** We have used the file Evaluation.csv provided for 2 test queries and we have created a ground_truth.csv with relevance scores for our 5 test queries.
- **Usage -->** The python notebook "project__part_2.py" was done in Google Colab, therefore it is recommended to download it and execute it using Colab. We divided
  the notebook into 3 main blocks.
  
### Block 0 (Loading) 
It's just meant to be executed to do all the imports we need and load data. 

### Block 1 (Indexing)
In this part, we will focus on indexing the cleaned data for efficient retrieval and analysis. We start by creating a basic index to retrieve only doc ids in which a term
appears, then we go through some initial test queries and finally work with a full tf-idf index. After computing and ranking tf-idf indices we decided to change to other test queries that we considered better for evaluation.

### Block 2 (Evaluation)
This section will cover the evaluation metrics used to assess the performance of our analysis methods. We start defining functions for every metric and then test result with the csv for the 2 queries provided and finally for ours. To finish the notebook, we represented the tweets in a 2D plot using TSNE and tf-idf vectors. This part of the code requires much RAM and time, so although can be executed it is not recommendable, as the .ipynb has the plot already.



## PART 3

- **Description -->** In the 3rd part of the project, we provide different rankings based on tf-idf + cosine similarity, our own scoring + cosine similarity, BM25 and using Word2Vec model.
- **Usage -->** The python notebook "project__part_3.py" was done in Google Colab, therefore it is recommended to download it and execute it using Colab. We divided
  the notebook into 3 main blocks.
  
### Block 0 (Loading) 
It's just meant to be executed to do all the imports we need and load data. 

### Block 1 (Scorings)
In this part, we reused our TF-IDF scoring system and combined it with cosine similarity to get a top-20 ranking of 2 test queries. Then, we created our own scoring based on popularity metrics such as number of likes, retweets, followers... and we combined it with the previous scoring to get another top-20. Finally, we made a top-20 ranking based on BM25 system and compared the similarities between the BM25 and the Tf-IDF systems.

### Block 2 (Word-2-Vec + Cosine Similarity)
This section covers the ranking of 5 test queries using a tweet-2-vec model using word2vec, this model is called tweetVec and can be used to compute the cosine similarity with each of the test queries to get the top-20 ranking for each of them.


## PART 4
The README for part 4 is inside the Project-Part-4 folder.
