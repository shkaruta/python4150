import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

# Загрузка данных
X = pd.read_csv("6_x.csv", header=None, delimiter=",", names=["x1", "x2", "x3"])
y = pd.read_csv("6_y.csv", header=None, delimiter=",", names=["y"])

# Объединяем для удобства X и y в один датафрейм по горизонтали (axis=1)
data = pd.concat([X, y], axis=1)

# Удаление выбросов
# вычисляет первый и третий квартили для каждой колонки
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)
# интерквартильный размах
IQR = Q3 - Q1
# удаляет выбросы из каждой колонки
data_cleaned = data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]

# Разделение данных после очистки
X_clean = data_cleaned[["x1", "x2", "x3"]]
y_clean = data_cleaned["y"]

# Разделение на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X_clean, y_clean, test_size=0.2, random_state=42)

# В список results будем записывать словари с результатами для всех моделей для финального вывода
results = []

def evaluate_model(model, X_test, y_test, label, features):
    # Функция вычисляет предикты для y, рассчитывает метрики модели, записывает результаты в result
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    results.append({
        "Regression": label,
        "Features": features,
        "R2": round(r2, 3),
        "MSE": round(mse, 1),
        "MAE": round(mae, 1),
        "MAPE": round(mape, 1)
    })

# Линейные регрессии для каждого признака
for i, col in enumerate(["x1", "x2", "x3"], start=1):
    model = LinearRegression()
    model.fit(X_train[[col]], y_train)
    evaluate_model(model, X_test[[col]], y_test, "Linear", f"x{i}")

# Множественная регрессия по всем признакам
multi_model = LinearRegression()
multi_model.fit(X_train, y_train)
evaluate_model(multi_model, X_test, y_test, "Linear", "x1+x2+x3")

# Множественная регрессия по второму и третьему признакам
subset_model = LinearRegression()
subset_model.fit(X_train[["x2", "x3"]], y_train)
evaluate_model(subset_model, X_test[["x2", "x3"]], y_test, "Linear", "x2+x3")

# Полиномиальные регрессии для каждого признака (степени 2 и 3)
for degree in [2, 3]:
    for i, col in enumerate(["x1", "x2", "x3"], start=1):
        poly_model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        poly_model.fit(X_train[[col]], y_train)
        evaluate_model(poly_model, X_test[[col]], y_test, f"Poly{degree}", f"x{i}")

# Вывод таблицы результатов
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
'''
Вывод программы.
Regression Features     R2     MSE   MAE  MAPE
    Linear       x1 -0.119 16118.5 100.8  96.0
    Linear       x2  0.866  1928.5  36.4  91.0
    Linear       x3  0.298 10114.8  80.1 124.6
    Linear x1+x2+x3  0.996    53.7   5.4   8.0
    Linear    x2+x3  0.997    49.8   5.0   9.3
     Poly2       x1 -0.231 17730.3 117.3 222.7
     Poly2       x2  0.871  1861.3  35.8  92.1
     Poly2       x3  0.298 10115.7  80.1 124.6
     Poly3       x1 -0.240 17868.3 117.8 242.3
     Poly3       x2  0.869  1889.9  35.5  90.8
     Poly3       x3  0.281 10361.5  81.7 135.4

     Объяснение результатов.
1. Использованные метрики.
R2 - доля вариаций целевой переменной, которую объясняет модель
MSE - среднеквадратичная ошибка
MAE - средняя ошибка в абсолютных значениях
MAPE - средняя абсолютная ошибка в процентах
2. Влияние признаков.
x1 практически не связан с целевой переменной, о чем говорит отрицательный R2.
x2 является основным драйвером зависимости целевой переменной. Линейная зависимость дает отличные результаты, полиномиальная лишь немного улучшает их.
x3 слабее чем x2 связан с целевой переменной, но в сочетании с x2 улучшает модель.
Множественная линейная регрессия x1+x2+x3 и x2+x3 дает примерно одинаковые результаты, но, поскольку x1 дает отрицательный R2 и не улучшает модель, им для простоты можно пренебречь.
Полиномиальная регрессия по одной переменной практически незначительно улучшает модель, третья степень не улучшает результаты по сравнению со второй.
Полиномиальная регрессия по нескольким переменным не улучшает результаты по сравнению с линейной (здесь эти результаты не приводятся), поэтому связь между переменными можно считать линейной.
3. Вывод.
Линейная модель по признакам x2+x3 отлично объясняет данные с коэффициентом детерминации 0.997, абсолютной ошибкой 5 единиц и 9 процентов.
'''