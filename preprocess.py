import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec
import numpy as np

# Function to preprocess a single file
def preprocess_file(file_path):
    # Load the data
    data = pd.read_json(file_path)

    # Handle missing data: drop the rows where at least one element is missing.
    data = data.dropna()

    # Handle outliers: for simplicity, let's consider 'viewCount' column
    Q1 = data['viewCount'].quantile(0.25)
    Q3 = data['viewCount'].quantile(0.75)
    IQR = Q3 - Q1

    filter = (data['viewCount'] >= Q1 - 1.5 * IQR) & (data['viewCount'] <= Q3 + 1.5 *IQR)
    data = data.loc[filter]  

    # Textual metadata into numerical features using TF-IDF
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(data.description).toarray()

    # Textual metadata into numerical features using Word2Vec
    # This requires the input to be in a format of list of words for each document (video description in this case)
    sentences = [desc.split(' ') for desc in data.description.tolist()]
    word2vec = Word2Vec(sentences, min_count=1)
    word2vec_features = np.array([word2vec[desc] for desc in sentences])

    # Save the preprocessed data back to the datasets folder
    preprocessed_file_path = file_path.replace('.json', '_preprocessed.json')
    data.to_json(preprocessed_file_path)


# Get a list of all the JSON files in the datasets directory
json_files = [f for f in os.listdir('datasets') if f.endswith('.json')]

# Preprocess each file
for file in json_files:
    preprocess_file(os.path.join('datasets', file))
