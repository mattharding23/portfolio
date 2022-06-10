import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import re
from wordcloud import WordCloud,STOPWORDS
from wordcloud import WordCloud
import plotly.express as px

#Read in data from Reddit Posts data frame
df = pd.read_csv("Data/Text_Data/Reddit Posts.csv")

#Removing stopwords and uninteresting words
stopwords= set(STOPWORDS)
uninteresting_words = {"the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just", "really",
                      "ve", "nan", "don", "xc", "got", "now", 'pr', 'much', 'around', 'still', 'th', 'even'}
stopwords = stopwords.union(uninteresting_words)
def preprocess_text(text): #this ensures that it only considers text, and not numbers
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    return text

#Vectorizing Data
MyCV = CountVectorizer(input='content', stop_words=stopwords, preprocessor=preprocess_text)
# tokenize and build vocab
dfVectorized = MyCV.fit_transform(df.body.values.astype('U'))
MyColumnNames=MyCV.get_feature_names_out()

#Creating data frame from the DTM
DF=pd.DataFrame(dfVectorized.toarray(), columns=MyColumnNames) 
DF.columns = DF.columns.str.replace('_', '')
DF = DF.append(DF.sum(numeric_only=True), ignore_index=True) #Adding a total at the bottom to generate word cloud from frequencies

#Melting the data so that we have words as the index
DF_melt = pd.melt(DF)
DF_melt = pd.melt(DF).groupby("variable").sum()
DF_melt.value = DF_melt.value / 2 #values seem doubled (likely due to the sum row we added at the  bottom), so we adjust by dividing by 2
DF_melt = DF_melt.sort_values("value", ascending=False)

#Building the Plotly bar graph
fig=px.bar(DF_melt.head(15), y='value', x=DF_melt.head(15).index,
      labels={"x": "Word", "value":"Frequency"})
# title alignment
fig.update_layout(plot_bgcolor = "#FAF0E6",
                  paper_bgcolor='#FAF0E6',
    title=dict(
        text='Word Frequency Bar Graph',
        x=0.5,
        font=dict(
            family="Arial",
            size=24,
            color='black'
        )
    ), 
    xaxis_title="Word",
    yaxis_title='Frequency',
    font=dict(
        family="Arial",
        size=18,
        color='black'
    )
)   
fig
fig.write_html("word-frequency.html")