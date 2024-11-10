import joblib
import numpy as np


class InflationManager:

    def __init__(self, current_year, current_month):
        self.current_year = current_year
        self.current_month = current_month

    def predict_inflation(self):
        model = joblib.load('inflation_model.joblib')

        base_year = 2014
        months_since_start = (self.current_year - base_year) * 12 + self.current_month

        future_prediction = model.predict(np.array([[months_since_start + 1]]))  # +1 для следующего месяца

        return future_prediction[0]

