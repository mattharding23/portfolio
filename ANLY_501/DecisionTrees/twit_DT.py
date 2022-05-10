#%% 
## LIBRARIES ------------------------------------------------
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import text 
import numpy as np
from numpy import savetxt
import pandas as pd
import os
import csv
import warnings
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from wordcloud import WordCloud
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random as rd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn import tree
import graphviz
from sklearn.decomposition import LatentDirichletAllocation 
from sklearn import preprocessing
import seaborn as sn
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D



warnings.filterwarnings('ignore')

#%%
# Use data cleaning code but add tfidf vectorizer

# DATA CLEANING

#-----------------

# Identify path to folder where tweets will be saved
path = '/Users/mattharding/Documents/Georgetown/Fall_2021/ANLY_501/Mod_2_assignment/'
path_csvs = path + 'tweet_csvs/'

# Retrieve names of csv files
csv_names=os.listdir(path_csvs)

path_txt = path + 'tweets/'

# save tweets as individual txt files & labels in a label list
labels = []
file_names = []
for file in csv_names:
    count = 1
    
    # Label is name of csv file not including '.csv'
    label = file.split('.')[0]
    
    # Read in csv file
    csv_read = csv.DictReader(open(f'{path_csvs}{file}'))
    
    for row in csv_read:
        
        # Extract text
        tweet = row['text']
        
        # Create filename variable
        fn = f'{path_txt}{label}{count}.txt'
        
        # Write tweet to txt file
        f = open(fn,'w')
        f.write(tweet)
        f.close()
        
        # Save label for tweet
        labels.append(label)
        
        # Save filename for count vectorizer
        file_names.append(fn)
        count += 1



# Create count vectorizer    
cv = CountVectorizer(input='filename',stop_words="english")
tv = TfidfVectorizer(input="filename", stop_words = "english")

# Get Document term matrix
dtm_cv = cv.fit_transform(file_names)
dtm_tv = tv.fit_transform(file_names)
# Extract column names
col_names_cv = cv.get_feature_names()
col_names_tv = tv.get_feature_names()

# Turn into pandas df
cv_df = pd.DataFrame(dtm_cv.toarray(),columns=col_names_cv)
tv_df = pd.DataFrame(dtm_tv.toarray(),columns=col_names_tv)


# Insert labels column
cv_df.insert(loc=0, column='Label', value=labels)
tv_df.insert(loc=0, column='Label', value=labels)

#remove number values
keep_words = [col for col in cv_df.columns if col.isalpha()]

cv_df = cv_df[keep_words]
tv_df = tv_df[keep_words]


# # Remove other words not caught by stopwords
more_stop_words = ['https','rt','ivepetthatdog']
keep_words = [col for col in cv_df.columns if not col in more_stop_words]
cv_df = cv_df[keep_words]
tv_df = tv_df[keep_words]

# chesapeake bay label is all encompassing and also has many more tweets than other labels. Will remove for now and ma
#ybe use as testing for laters. 
cv_dt_df = cv_df[cv_df['Label'] != 'chesapeakebay']
tv_dt_df = tv_df[tv_df['Label'] != 'chesapeakebay']

# Save dfs to csvs
cv_dt_df.to_csv('Labeled_cv_data.csv')
tv_dt_df.to_csv('Labeled_tv_data.csv')

#%% Decision Tree on Count Vectorizer Data

# Split into testing & training dataframes
train_set, test_set = train_test_split(cv_dt_df, test_size=0.3)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create decision tree model
model = DecisionTreeClassifier(criterion='entropy', 
                            splitter='best',  
                            random_state=11, 
                            min_samples_split=2, 
                            min_samples_leaf=1,
                            ccp_alpha = .0425)

# Fit data to model
model.fit(train_set, train_labs)

# Plot decision tree
figure1= plt.gcf()
figure1.set_size_inches(12, 10)
tree.plot_tree(model, filled = True, label = 'all',feature_names = train_set.columns.to_list())
plt.savefig('tweet_tree_cv.png')


# test model by predicting labels of test set
model_pred=model.predict(test_set)

# Ctreate confusion Matrix
model_cm = confusion_matrix(test_labs, model_pred)
print("\nThe confusion matrix is:")
print(model_cm)

# Save confusion matrix to csv for creating visual. 
savetxt('cv_cm.csv', model_cm, delimiter=',')


# Get feature importances 
feature_names=train_set.columns
FeatureImp=model.feature_importances_   
indices = np.argsort(FeatureImp)[::-1]
## print out the important features.....
imp = []
feat = []
for f in range(train_set.shape[1]):
    if FeatureImp[indices[f]] > 0:
        imp.append( FeatureImp[indices[f]])
        feat.append(feature_names[indices[f]])
feat_imp = pd.DataFrame(
    {'Feature': feat,
     'Importance': imp,
    })

# Save feature importances for creating visual. 
feat_imp.to_csv('cv_feat_imp.csv')




#%% Decision tree for TFIDF vectorizer data

# Split into testing & training dataframes
train_set, test_set = train_test_split(tv_dt_df, test_size=0.35)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create decision tree model
model = DecisionTreeClassifier(criterion='entropy', 
                            splitter='best',  
                            random_state=11, 
                            min_samples_split=2, 
                            min_samples_leaf=1,
                            ccp_alpha = .04)

# Fit data to model
model.fit(train_set, train_labs)

# Plot decision tree
figure2= plt.gcf()
figure2.set_size_inches(12, 10)
tree.plot_tree(model, filled = True, label = 'all',feature_names = train_set.columns.to_list())
plt.savefig('tweet_tree_tv.png')


# test model by predicting labels of test set
model_pred=model.predict(test_set)

# Ctreate confusion Matrix
model_cm = confusion_matrix(test_labs, model_pred)
print("\nThe confusion matrix is:")
print(model_cm)

# Save confusion matrix to csv for creating visual. 
savetxt('tv_cm.csv', model_cm, delimiter=',')

# Get feature importances 
feature_names=train_set.columns
FeatureImp=model.feature_importances_   
indices = np.argsort(FeatureImp)[::-1]
## print out the important features.....
imp = []
feat = []
for f in range(train_set.shape[1]):
    if FeatureImp[indices[f]] > 0:
        imp.append( FeatureImp[indices[f]])
        feat.append(feature_names[indices[f]])
feat_imp = pd.DataFrame(
    {'Feature': feat,
     'Importance': imp,
    })

# Save feature importances for creating visual. 
feat_imp.to_csv('tv_feat_imp.csv')


#%% IF overall label is left in

# Split into testing & training dataframes
train_set, test_set = train_test_split(cv_df, test_size=0.4)

# Remove and save labels from test data
test_labs = test_set['Label']
test_set = test_set.drop(['Label'], axis=1)

# Separate labels from training set
train_labs = train_set['Label']
train_set = train_set.drop(['Label'], axis=1)

# Create decision tree model
model = DecisionTreeClassifier(criterion='entropy', 
                            splitter='best',  
                            random_state=11, 
                            min_samples_split=2, 
                            min_samples_leaf=1,
                            ccp_alpha = .0125)

# Fit data to model
model.fit(train_set, train_labs)

# Plot decision tree
figure3 = plt.gcf()
figure3.set_size_inches(12, 10)
tree.plot_tree(model, filled = True, label = 'all',feature_names = train_set.columns.to_list())
plt.savefig('tweet_tree_all.png')


# test model by predicting labels of test set
model_pred=model.predict(test_set)

# Ctreate confusion Matrix
model_cm = confusion_matrix(test_labs, model_pred)
print("\nThe confusion matrix is:")
print(model_cm)

# Save confusion matrix to csv for creating visual. 
savetxt('all_cm.csv', model_cm, delimiter=',')

# Get feature importances 
feature_names=train_set.columns
FeatureImp=model.feature_importances_   
indices = np.argsort(FeatureImp)[::-1]
## print out the important features.....
imp = []
feat = []
for f in range(train_set.shape[1]):
    if FeatureImp[indices[f]] > 0:
        imp.append( FeatureImp[indices[f]])
        feat.append(feature_names[indices[f]])
feat_imp = pd.DataFrame(
    {'Feature': feat,
     'Importance': imp,
    })

# Save feature importances for creating visual. 
feat_imp.to_csv('all_feat_imp.csv')