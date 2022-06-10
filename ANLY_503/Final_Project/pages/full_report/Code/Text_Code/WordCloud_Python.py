import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import re
from wordcloud import WordCloud,STOPWORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

#Read in data from Reddit Posts data frame
df = pd.read_csv("Data/Text_Data/Reddit Posts.csv")

#Removing stopwords and uninteresting words
stopwords= set(STOPWORDS)
uninteresting_words = {"the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my",     "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them",     "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being",     "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how",     "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just", "really",
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

#Word Cloud Code
mask = np.array(Image.open('RunningMan.png'))
wc = wordcloud = WordCloud(background_color="white", 
                      stopwords=stopwords,
                      mask=mask,
                      max_words=40, 
                      min_word_length=3,
                      collocations=False,
                      random_state=1,
                      colormap='Dark2',
                      font_path='arial',
                      contour_color='steelblue',contour_width=2).generate_from_frequencies(DF.iloc[len(DF)-1])
plt.figure(figsize=(20,20))
plt.text(x=100, y=-70, fontsize=29,
         s='Fig. 1: Most Frequent Words from Reddit')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
#wc.to_file('worccloud.png')
plt.savefig('worccloud2.png')

