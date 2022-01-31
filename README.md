# offensive-meme-categorizer
Detect memes that are part of a specific offensive category

This project consists of 2 main parts:

## 1. Labeled data extraction and interpretation
Project is located [here](nlp).

See [`analyze_results/analyze_kappa.py`](analyze_results/analyze_kappa.py)
for a usage example, including Fleiss' Kappa and Kendall's Tau analysis.

## 2. Predictive model
See [`nlp/categorizer/create_model.py`](nlp/categorizer/create_model.py)
for a usage example, including the creation of `LogisticRegression`, `MLPRegressor` and `MLPClassifier` based models.
