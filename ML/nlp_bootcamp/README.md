## Sentimental analysis bootcamp

The assessment of the bank by the text feedback of the client predicting [competition](https://www.kaggle.com/competitions/hse-nlp-bootcamp/overview).

## Main steps

1. Lemmatization of text data *(taken from the baseline)*; 
2. Creating date-based features;
3. Creating number of words and length of feedback features; 
4. Text data encoding:
   - TF-IDF Vectorization with ngram_range=(1, 3); 
   - Count Vectorization on the default parameters;
   - Count Vectorization with ngram_range=(1, 2).
5. Fitting **LightGBMClassifrier** on each part of data from 4th point and predicting testing data;
6. Averaging probabilities of each class and choosing the class highest probability with.

## Metrics
The metric of competition is F1(micro).

Public leaderboard: 0.79581;

Private leaderboard: 0.79419.