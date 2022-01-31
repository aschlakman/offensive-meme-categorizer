# Based on tutorial: 
# https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/

import pickle
import pandas as pd
from sklearn import metrics
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
# Logistic Regression Classifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.base import BaseEstimator

from categorizer.transformer import predictors
from categorizer.vectorizer import bow_vector

MEMES_RATED_JSON = r'..\..\analyze_results\rated_memes.json'

def create_model(estimator_algorithm: 'BaseEstimator' = None, is_continuous = False):
    print('Continuous mode: ', is_continuous)

    with open(MEMES_RATED_JSON, 'r') as rated_memes_file:
        df_memes = pd.read_json(rated_memes_file)

    df_memes = df_memes.transpose()

    X = df_memes['text'] # the features we want to analyze

    if not is_continuous:
        ylabels = df_memes['target_harmful'] # the labels, or answers, we want to test against
        ylabels = ylabels.astype(bool)

        print('Harmful memes:')
        print(df_memes.target_harmful.value_counts())
    else:
        ylabels = df_memes['target_avg'] # the labels, or answers, we want to test against
        ylabels = ylabels.astype(float)


    X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size=0.3)

    if estimator_algorithm is None:
        estimator_algorithm = LogisticRegression()

    # Create pipeline using Bag of Words
    pipe = Pipeline([("cleaner", predictors()),
                     ('vectorizer', bow_vector),
                     ('estimator', estimator_algorithm)])

    # model generation
    pipe.fit(X_train,y_train)

    # Predicting with a test dataset
    predicted = pipe.predict(X_test)

    if not is_continuous:
        # Model Accuracy
        print("Accuracy:",metrics.accuracy_score(y_test, predicted))
        print("Precision:",metrics.precision_score(y_test, predicted))
        print("Recall:",metrics.recall_score(y_test, predicted))
        print("Cohens Kappa:", metrics.cohen_kappa_score(y_test, predicted))
    else:

        print("RMSE:", metrics.mean_squared_error(y_test, predicted, squared=False))
    return pipe


def save_model(model, filename):
    with open(filename, 'wb') as out_file:
        pickle.dump(model, out_file)

def load_model(filename):
    with open(filename, 'rb') as in_file:
        model = pickle.load(in_file)
    return model

if __name__ == '__main__':
    print('LogisticRegression')
    model = create_model(LogisticRegression())
    save_model(model, 'saved_models/LogisticRegression.pickle')

    print('MLPRegressor')
    model = create_model(MLPRegressor(random_state=1, max_iter=500), True)
    save_model(model, 'saved_models/MLPRegressor.pickle')

    print('MLPClassifier')
    model = create_model(MLPClassifier(random_state=1, max_iter=500), False)
    save_model(model, 'saved_models/MLP_Classifier2.pickle')
