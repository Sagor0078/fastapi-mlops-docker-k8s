# Import packages
import gzip

import joblib
import pandas as pd
from sklearn.ensemble import VotingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

# Load the dataset
data = pd.read_csv("data/breast_cancer.csv")

# Preselected feature
selected_features = [
    "concavity_mean",
    "concave_points_mean",
    "perimeter_se",
    "area_se",
    "texture_worst",
    "area_worst",
]

# Preprocess dataset
data = data.set_index("id")
data["diagnosis"] = data["diagnosis"].replace(
    ["B", "M"], [0, 1]
)  # Encode y, B -> 0 , M -> 1

# Split into train and test set, 80%-20%
y = data.pop("diagnosis")
X = data
X = X[selected_features.copy()]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create an ensemble of 3 models
estimators = [
    ("logistic", LogisticRegression()),
    ("cart", DecisionTreeClassifier()),
    ("svm", SVC()),
]

# Create the Ensemble Model
ensemble = VotingClassifier(estimators)

# Make preprocess Pipeline
pipe = Pipeline(
    [
        ("imputer", SimpleImputer()),  # Missing value Imputer
        ("scaler", MinMaxScaler(feature_range=(0, 1))),  # Min Max Scaler
        ("model", ensemble),  # Ensemble Model
    ]
)

# Train the model
pipe.fit(X_train, y_train)

# Test Accuracy
print(f"Accuracy: {round(pipe.score(X_test, y_test))*100}")

# Export model
joblib.dump(pipe, gzip.open("model/model_binary.dat.gz", "wb"))
