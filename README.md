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
In this last block, we perform a data analysis separately for tweets and translated_tweets, creating charts and lists of the most retweeted tweets, most used words or hashtags,
wordclouds, and entity recognition. This last section requires loading the Spacy model for English, and it's a little time-consuming. All cells must be run in order.


## PART 2

### Indexing
In this part, we will focus on indexing the cleaned data for efficient retrieval and analysis. Details on the indexing process, including the tools and libraries used, will be provided here.

### Evaluation
This section will cover the evaluation metrics used to assess the performance of our analysis methods. We'll discuss the criteria for measuring success and the outcomes derived from our analyses.
