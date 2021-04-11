import joblib
import pandas as pd


class RandomForestClassifier:
    def __init__(self):
        self.model = joblib.load("research/random_forest.joblib")
        self.ohe_col = joblib.load("research/all_columns.joblib")
        self.values_fill_missing = joblib.load("research/train_mode.joblib")

    def predict(self, input_data):
        return self.model.predict_proba(input_data)

    def preprocessing(self, input_data):
        input_data = pd.DataFrame(input_data, index=[0])
        input_data.fillna(self.values_fill_missing)
        input_data = self.ohe_values(input_data)

        return input_data

    def ohe_values(self, input_data):
        cat_columns = [
            "Gender",
            "Married",
            "Education",
            "Self_Employed",
            "Property_Area",
        ]
        df_processed = pd.get_dummies(input_data, columns=cat_columns)
        new_dict = {}

        for i in self.ohe_col:
            if i in df_processed.columns:
                new_dict[i] = df_processed[i].values
            else:
                new_dict[i] = 0

        new_df = pd.DataFrame(new_dict)
        return new_df

    def postprocessing(self, input_data):
        label = "Rejected"
        if input_data[1] > 0.5:
            label = "Approved"
        return {"probability": input_data[1], "label": label, "status": "OK"}

    def get_accuracy(self, x, y):
        return self.model.score(x, y)

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)[0]
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
