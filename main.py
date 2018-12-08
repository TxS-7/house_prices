#!/usr/bin/python
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LassoLars, ElasticNet, LinearRegression
from sklearn.svm import SVR
from sklearn.metrics.scorer import make_scorer
from sklearn.model_selection import cross_val_score
import math

# https://en.wikipedia.org/wiki/Root-mean-square_deviation
# Need to return negative because greater_is_better=False flips the sign
def rmse(predicted, correct):
    total = 0
    i = 0
    for pred in predicted:
        diff = (math.log(pred, 10) - math.log(correct[i], 10))
        #diff = (pred - correct[i])
        total += diff * diff
        i += 1
    return -math.sqrt(total / len(predicted))


def create_df(filename):
    # Read the train set
    df = pd.read_csv(filename)

    df['TotalBsmtSF'].fillna(df['TotalBsmtSF'].mean(), inplace=True)
    df['GarageCars'].fillna(df['GarageCars'].median(), inplace=True)

    return df


def run(train_data):
    features = ["OverallQual", "TotalBsmtSF", "GrLivArea", "GarageCars", "YearRemodAdd"]
    target = train_data['SalePrice']

    reg = RandomForestRegressor(n_estimators=50)
    #reg = LinearRegression()

    # Perform 10-fold cross validation to evaluate the classifier
    rmse_scorer = make_scorer(rmse, greater_is_better=False)
    scores = cross_val_score(reg, train_data[features], target, cv=10, scoring=rmse_scorer)
    return list(scores)


def predict(train_data, test_data):
    features = ["OverallQual", "TotalBsmtSF", "GrLivArea", "GarageCars", "YearRemodAdd"]
    target = train_data['SalePrice']

    reg = RandomForestRegressor(n_estimators=50)
    reg.fit(train_data[features], target)
    predictions = reg.predict(test_data[features])

    print "[+] Writing results to predictions.csv"
    pd.DataFrame({"Id": test_data['Id'], "SalePrice": predictions}).to_csv("predictions.csv", index=False)


if __name__ == "__main__":
    train_data = create_df("train.csv")

    if raw_input("Perform cross validation of train.csv? (y/n)\n> ") == "y":
        scores = run(train_data)
        print "[*] 10-fold cross validation results:"
        for val in scores:
            print "\t" + str(val)
        print "[*] Average: " + str(sum(scores) / float(len(scores)))

    if raw_input("Perform prediction of test.csv? (y/n)\n> ") == "y":
        test_data = create_df("test.csv")
        predict(train_data, test_data)
