# Задача классификации на датасете wine из библиотеки sklearn
# Обучены модели логистическая регрессия, svm, knn, random forest, многослойный персептрон

from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
import pandas as pd

# 1. Загрузка данных
data = load_wine()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# 2. Проверка типов данных и пропусков
print(df.info())
missing_data = df.isnull().sum()
print(f"Общее количество пропущенных значений: {missing_data.sum()}")

# 3. Удаление выбросов
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
df_no_outliers = df[~((df < (Q1 - 2.0 * IQR)) | (df > (Q3 + 2.0 * IQR))).any(axis=1)]
print(f"Количество строк до удаления выбросов: {df.shape[0]}")
print(f"Количество строк после удаления выбросов: {df_no_outliers.shape[0]}")

# 4. Стандартизация данных
scaler = StandardScaler()
features = df_no_outliers.drop(columns=['target'])
scaled_features = scaler.fit_transform(features)
df_scaled = pd.DataFrame(scaled_features, columns=features.columns)
df_scaled['target'] = df_no_outliers['target'].values

# 5. Разделение данных
X = df_scaled.drop(columns=['target'])
y = df_scaled['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Обучение моделей
models = {
    "Logistic Regression": LogisticRegression(max_iter=10000, random_state=42),
    "SVM": SVC(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Random Forest": RandomForestClassifier(random_state=42),
    "MLP": MLPClassifier(random_state=42, max_iter=1000)
}

# Словарь для хранения результатов
results = {}

# Цикл по моделям: обучение, предсказание, оценка
for model_name, model in models.items():
    # Обучение модели
    model.fit(X_train, y_train)
    
    # Предсказания
    y_pred = model.predict(X_test)
    
    # Сохранение метрик
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    confusion = confusion_matrix(y_test, y_pred)
    results[model_name] = {
        "Accuracy": accuracy,
        "F1-score": f1,
        "Confusion Matrix": confusion
    }
    
# 7. Вывод результатов
for model_name, metrics in results.items():
    print(f"\n{model_name}:")
    print(f"  Accuracy: {metrics['Accuracy']:.3f}")
    print(f"  F1-score: {metrics['F1-score']:.3f}")
    print(f"  Confusion Matrix:\n{metrics['Confusion Matrix']}")

# 8. Выбор лучшей модели
sorted_results = sorted(results.items(), key=lambda x: (x[1]["F1-score"], x[1]["Accuracy"]), reverse=True)
print("\nЛучшая модель:")
best_f1_score = sorted_results[0][1]["F1-score"]
best_accuracy = sorted_results[0][1]["Accuracy"]
for model_name, metrics in sorted_results:
    if metrics["F1-score"] == best_f1_score and metrics["Accuracy"] == best_accuracy:
        print(f"{model_name}: F1-score = {metrics['F1-score']:.3f}")

'''
Вывод программы.
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 178 entries, 0 to 177
Data columns (total 14 columns):
 #   Column                        Non-Null Count  Dtype
---  ------                        --------------  -----
 0   alcohol                       178 non-null    float64
 1   malic_acid                    178 non-null    float64
 2   ash                           178 non-null    float64
 3   alcalinity_of_ash             178 non-null    float64
 4   magnesium                     178 non-null    float64
 5   total_phenols                 178 non-null    float64
 6   flavanoids                    178 non-null    float64
 7   nonflavanoid_phenols          178 non-null    float64
 8   proanthocyanins               178 non-null    float64
 9   color_intensity               178 non-null    float64
 10  hue                           178 non-null    float64
 11  od280/od315_of_diluted_wines  178 non-null    float64
 12  proline                       178 non-null    float64
 13  target                        178 non-null    int64
dtypes: float64(13), int64(1)
memory usage: 19.6 KB
None
Общее количество пропущенных значений: 0
Количество строк до удаления выбросов: 178
Количество строк после удаления выбросов: 173
Logistic Regression:
  Accuracy: 1.000
  F1-score: 1.000
  Confusion Matrix:
[[16  0  0]
 [ 0 12  0]
 [ 0  0  7]]
SVM:
  Accuracy: 1.000
  F1-score: 1.000
  Confusion Matrix:
[[16  0  0]
 [ 0 12  0]
 [ 0  0  7]]
KNN:
  Accuracy: 0.943
  F1-score: 0.944
  Confusion Matrix:
[[16  0  0]
 [ 0 10  2]
 [ 0  0  7]]
Random Forest:
  Accuracy: 1.000
  F1-score: 1.000
  Confusion Matrix:
[[16  0  0]
 [ 0 12  0]
 [ 0  0  7]]
MLP:
  Accuracy: 0.971
  F1-score: 0.972
  Confusion Matrix:
[[16  0  0]
 [ 0 11  1]
 [ 0  0  7]]
Лучшая модель:
Logistic Regression: F1-score = 1.000
SVM: F1-score = 1.000
Random Forest: F1-score = 1.000
'''
'''
Описание работы программы.
1. Датасет представляет собой 178 записей, 13 признаков, целевую переменную с тремя классами.
Данные хорошо сбалансированы по классам.
Пропусков нет.
За границы 1.5 * iqr выходит около 10% данных, для удаления выбросов использован коэффициент 2.
Данные масштабированы при помощи StandardScaler().
2. Для оценки качества моделей выбраны метрики:
accuracy - доля правильных предсказаний среди всех предсказаний,
F1-score - среднее гармоническое между precision (минимизирует ложные срабатывания) и recall (минимизирует пропуски объектов),
confusion matrix - матрица ошибок.
Метриками fp и fn можно пренебречь, т.к. они учитываются в F1-score и не являются критическими для классификации вин.
3. Выбор лучшей модели.
Датасет небольшой по объему, данные сбалансированы, все модели показали высокие и схожие результаты.
После нескольких экспериментов с выбросами и разным разделением выборки на обучающую и тестовую можно сказать, что из 5 моделей лучшие результаты показали:
логическая регрессия
метод опорных векторов
random forest
'''
