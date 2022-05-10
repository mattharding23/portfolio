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