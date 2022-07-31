"""
This code:
- performs text cleaning for Amazon Alexa reviews: remove punctuation, remove stop words, convert to lower case
- draws word clouds for positive and negative reviews
- train three machine learning models to predict ratings based on review texts
- test machine learning models' performances

The code is adapted from a hands-on project NLP: Twitter Sentiment Analysis
https://www.coursera.org/projects/twitter-sentiment-analysis

Data source: https://www.kaggle.com/datasets/sid321axn/amazon-alexa-reviews

Author: Woramon P.
Date: 07/31/2022
"""

# If running for the first time, use the NLTK Downloader to obtain the resource:
# import nltk
# nltk.download('stopwords')

from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier


def clean_text(text: str) -> str:
    """
    This function cleans up the text: remove punctuation, convert to lower case, remove stop words
    """
    removed_punc = ''.join([char for char in text if char not in string.punctuation])
    removed_punc = removed_punc.lower()
    removed_punc_stopwords = ' '.join([word for word in removed_punc.split()
                                      if word not in stopwords.words('english')])
    return removed_punc_stopwords


def group_rating(rating: int) -> str:
    """
    This function groups ratings of 1, 2, 3 into "low_rating" and 4, 5 into "high_rating".
    """
    if rating in [1, 2, 3]:
        return 'low_rating'
    elif rating in [4, 5]:
        return 'high_rating'
    else:  # in case there is missing data
        return ''


# Load the data, clean up the text, drop rows without reviews, drop unused columns
df = pd.read_csv('amazon_reviews.csv')
df['reviews_cleaned'] = df['verified_reviews'].apply(clean_text)
df['rating_grouped'] = df['rating'].apply(group_rating)
df = df.replace('', np.nan)
df = df.dropna(axis=0, how='any')
df = df.drop(['date', 'variation', 'verified_reviews'], axis=1)

# Split negative and positive reviews
negative = df[df['rating_grouped'] == 'low_rating']
positive = df[df['rating_grouped'] == 'high_rating']

# Convert negative reviews to list format
negative_sentences = negative['reviews_cleaned'].tolist()
# Join all reviews into one large string
negative_one_string = ' '.join(negative_sentences)
# Draw word cloud
plt.figure(figsize=(8, 5))
plt.imshow(WordCloud().generate(negative_one_string))
plt.savefig('wordcloud_negative_reviews.jpg')

# Draw word cloud for positive reviews
positive_sentences = positive['reviews_cleaned'].tolist()
positive_one_string = ' '.join(positive_sentences)
plt.imshow(WordCloud().generate(positive_one_string))
plt.savefig("wordcloud_positive_reviews.jpg")

# Convert a collection of text documents to a matrix of token counts
vectorizer = CountVectorizer()
reviews_count_vectorizer = vectorizer.fit_transform(df['reviews_cleaned'])
review_texts = pd.DataFrame(reviews_count_vectorizer.toarray())
review_ratings = df['rating_grouped']

# Train AI/ML model using multinomial Naive Bayes classifier
text_train, text_test, rating_train, rating_test = train_test_split(review_texts, review_ratings, test_size=0.2)
model_NB = MultinomialNB()
model_NB.fit(text_train, rating_train)
# Predict the test set results
rating_predicted_NB = model_NB.predict(text_test)
print("\nMultinomial Naive Bayes classifier results\n")
print(classification_report(rating_test, rating_predicted_NB))
# Read here for explanation on the classification report:
# https://medium.com/@kohlishivam5522/understanding-a-classification-report-for-your-machine-learning-model-88815e2ce397
# https://towardsdatascience.com/choosing-performance-metrics-61b40819eae1

# Train AI/ML model using Logistic Regression (aka logit, MaxEnt) classifier
model_LR = LogisticRegression()
model_LR.fit(text_train, rating_train)
rating_predicted_LR = model_LR.predict(text_test)
print("\nLogistic Regression classifier results\n")
print(classification_report(rating_test, rating_predicted_LR))

# Train AI/ML model using Gradient Boosting classifier
# The part takes longer time to run.
model_GB = GradientBoostingClassifier()
model_GB.fit(text_train, rating_train)
rating_predicted_GB = model_GB.predict(text_test)
print("\nGradient Boosting classifier results\n")
print(classification_report(rating_test, rating_predicted_GB))
