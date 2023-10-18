import os
import pickle
import random
import json
import pandas as pd
import numpy as np
from pathlib import Path
import xgboost as xgb
from sklearn import metrics
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return json.JSONEncoder.default(self, obj)


def train():
    with open(os.path.join(BASE_DIR, 'app/ML/log.txt'), 'w+') as log_file:
        train_df = pd.read_csv(os.path.join(BASE_DIR, 'temp/data.csv'), index_col=[0])

        log_file.write(f'=> Количество строк и столбцов в датасете: {train_df.shape[0]}; {train_df.shape[1]}\n')

        y = train_df['SalePrice']
        train_df.drop(columns=['SalePrice'], axis=1, inplace=True)
        X = train_df
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        log_file.write(f'=> Размер тренировочной выборки: {len(X_train)}\n')
        log_file.write(f'=> Размер тестовой выборки: {len(X_test)}\n')

        model = xgb.XGBRegressor(max_depth=20, n_estimators=500, learning_rate=0.1, random_state=0)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        log_file.write(f'=> Mean Absolute Error: {metrics.mean_absolute_error(y_test, y_pred)}\n')
        log_file.write(f'=> Mean Squared Error: {metrics.mean_squared_error(y_test, y_pred)}\n')
        log_file.write(f'=> Root Mean Squared Error: {np.sqrt(metrics.mean_squared_error(y_test, y_pred))}\n')

        with open(os.path.join(BASE_DIR, 'app/ML/XGBmodel.dat'), 'wb') as f:
            pickle.dump(model, f)

        log_file.write(f'=> Модель успешно обучена')


def use():
    test_df = pd.read_csv(os.path.join(BASE_DIR, 'temp/data.csv'), index_col=[0])
    str_count = test_df.shape[0] - 1
    random_num = random.randint(1, str_count)
    random_str = test_df.iloc[random_num]
    target = random_str['SalePrice']
    test_df.drop(columns=['SalePrice'], axis=1, inplace=True)
    random_str = test_df.iloc[random_num]
    str_for_predict = pd.DataFrame([random_str.values], columns=test_df.columns)
    test_data = dict(zip(test_df.columns, random_str.values))
    test_data = json.dumps(test_data, indent=4, cls=NpEncoder)
    with open(os.path.join(BASE_DIR, 'app/ML/XGBmodel.dat'), 'rb') as f:
        model = pickle.load(f)
        prediction = str(round(np.expm1(model.predict(str_for_predict))[0], 2) / 10000)
    return target, test_data, prediction


