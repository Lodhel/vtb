import pandas as pd
import joblib  


class CalculateManager:
    model_path = 'xgboost_model.joblib'

    def calculate(self):
        loaded_model = self.load_model(self.model_path)

        # Пример новых данных, которые вы хотите предсказать
        # Убедитесь, что новые данные содержат те же признаки, что и в обучающей выборке
        new_data = pd.DataFrame({
            'income': [50000],  # Пример дохода
            'expense': [30000],  # Пример расходов
            'count_child': [1],  # Например, 1 ребенок
            'curs_dollar': [75],  # Курс доллара
            'curs_euro': [85],    # Курс евро
            'curs_uan': [15],     # Курс юаня
            'oil_brent': [70],    # Цена на нефть Brent
            'rate': [5],          # Процентная ставка
            'inf': [3],           # Уровень инфляции
            'education': ['высшее'],  # Уровень образования (категориальный признак)
            'work': ['госслужащий'],  # Вид работы (категориальный признак)
            'married': ['женат'],      # Семейное положение (категориальный признак)
            'year': [2021],            # Год (если хотите его использовать)
            'month': [5]               # Месяц (если хотите его использовать)
        })

        # Использование модели для предсказания
        predicted_savings = loaded_model.predict(new_data)

        return predicted_savings[0]

    @staticmethod
    def load_model(model_path):
        return joblib.load(model_path)
