import pandas as pd
import model


def predict(X, classifier):
    prediction = classifier.predict(X)[0]
    return prediction


def get_model_response(sample):
    X = pd.json_normalize(sample.__dict__)
    prediction = predict(X, model)
    label = "M" if prediction == 1 else "B"
    return {"label": label, "prediction": int(prediction)}
