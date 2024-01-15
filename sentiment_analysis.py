#  Importing Libraries
import wordcloud
from wordcloud import WordCloud, STOPWORDS

from textblob import TextBlob
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm


#  Loading the reviews
with open("reviews.txt", "r", encoding="utf-8") as f:
   reviews = f.readlines()
    
#  Preprocessing the text
import re
def preprocess_review(review):
    review = re.sub(r"[^a-zA-Z0-9]", " ", review)  # removing irrelevant symbols and punctuation
    review = review.lower()  # Converting to lowercase
    words = review.split()  # splitting into words
    stop_words = set(stopwords.words("english"))  # removing stop words
    words = [word for word in words if word not in stop_words]
    return " ".join(words)  # rejoining words into a string

#  Analysing Sentiments
def classify_sentiment(sentiment_score):
  if sentiment_score > 0.3:
    return "Positive"
  elif sentiment_score < -0.3:
    return "Negative"
  else:
    return "Neutral"

#  Preparing data for dataframe
reviews = []
sentiment_scores =[]
sentiment_categories = []

with open("reviews.txt", "r", encoding="utf-8") as f:
   for review in f.readlines():
      
      processed_review = preprocess_review(review)
      # handle empty strings
      if processed_review:
        blob = TextBlob(processed_review)
        sentiment = blob.sentiment.polarity
        category = classify_sentiment(sentiment)

        reviews.append(review)
        sentiment_scores.append(sentiment)
        sentiment_categories.append(category)

#  Converting Data to dataframe
df = pd.DataFrame({
   "Review": reviews,
   "Sentiment Score": sentiment_scores,
   "Sentiment Category": sentiment_categories
})

#  Creating bar graph

sentiment_counts = df["Sentiment Category"].value_counts() # Extracting category counts from dataframe
colors = ["green", "yellow", "red"]

plt.figure(figsize=(10, 7))
plt.bar(sentiment_counts.index, sentiment_counts.values, color = colors)

plt.xlabel("Sentiment Category")
plt.ylabel("Frequency")
plt.title("Sentiment Distribution of Reviews")
plt.show()

# Creating sentiment-based wordcloud

textblobs = [TextBlob(review) for review in reviews]

def color_func(word, font_size, position, orientation, random_state =None, **kwargs):
   if word in reviews:
        sentiment = textblobs[reviews.index(word)].sentiment.polarity
        if sentiment > 0.5:  # Adjust thresholds as needed
            return "green"
        elif sentiment > 0.1:
            return "lightgreen"
        elif sentiment > -0.1:
            return "yellow"
        elif sentiment > -0.5:
            return "orange"
        else:
            return "red"
   else:
        return "gray"
   
wordcloud = WordCloud(
   width = 800, height = 600, margin= 5,
   background_color="white", colormap= "viridis",
   collocations= False,
   stopwords= STOPWORDS,
   color_func= color_func
).generate(" ".join(reviews))

wordcloud.to_image().show()


