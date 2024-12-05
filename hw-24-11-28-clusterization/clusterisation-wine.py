# Кластеризация на датасете wine из библиотеки sklearn
# Использованы алгоритмы kmeans, gmm, spectral, dbscan, agglomerative с разными параметрами
# для каждого алгоритма выбран лучший вариант
# результаты кластеризации визуализированы
# сделана визуализация pca
# в конце файла показан вывод программы на печать, объяснение выбора алгоритмов, метрик и лучшей модели

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score, davies_bouldin_score, adjusted_rand_score, normalized_mutual_info_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt

# Загрузка данных
from sklearn.datasets import load_wine
data = load_wine()
X = pd.DataFrame(data.data, columns=data.feature_names)
y_true = data.target

# 1. Исследование корреляции признаков
corr_matrix = X.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Корреляционная матрица признаков")
plt.show()

# Удаление высоко коррелированных признаков
# Оказалось, что удаление единственного коррелирующего признака привело к снижению ari для kmeans, поэтому лучше признак оставить
# print("\nКоррелирующие признаки (порог = 0.85):")
# high_corr = corr_matrix[(corr_matrix > 0.85) & (corr_matrix < 1.0)].stack()
# print(high_corr)
# X = X.drop(columns=["total_phenols"])  # Удаляем коррелированный признак

# 2. Стандартизация данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 3. Уменьшение размерности для визуализации (PCA)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, cmap='viridis', s=50)
plt.title("PCA: Истинные метки классов")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

# Функция для выбора лучшей модели с учетом ARI, затем Silhouette
def select_best_model(results_df):
    return results_df.sort_values(by=["ARI", "Silhouette"], ascending=[False, False]).iloc[0]

# Функция для вывода результатов
def evaluate_clustering(model_name, labels, X, y_true):
    if len(np.unique(labels)) <= 1:
        return {"Model": model_name, "Silhouette": np.nan, "DB Index": np.nan, "ARI": 0, "NMI": 0}
    silhouette = silhouette_score(X, labels)
    db_index = davies_bouldin_score(X, labels)
    ari = adjusted_rand_score(y_true, labels)
    nmi = normalized_mutual_info_score(y_true, labels)
    return {"Model": model_name, "Silhouette": round(silhouette, 3), "DB Index": round(db_index, 3), "ARI": round(ari, 3), "NMI": round(nmi, 3)}

# Единый список для всех результатов
results = []

# 4. K-Means
# проверим для разного числа кластеров
for k in [2, 3, 4]:
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels_kmeans = kmeans.fit_predict(X_scaled)
    results.append(evaluate_clustering(f"K-Means (k={k})", labels_kmeans, X_scaled, y_true))

# 5. Agglomerative Clustering
# попробуем разные стратегии объединения кластеров (linkage)
for linkage in ['ward', 'complete', 'average', 'single']:
    agglo = AgglomerativeClustering(n_clusters=3, linkage=linkage)
    labels_agglo = agglo.fit_predict(X_scaled)
    results.append(evaluate_clustering(f"Agglomerative (linkage={linkage})", labels_agglo, X_scaled, y_true))

# 6. DBSCAN
# разные варианты dbscan (можно и не проверять, сразу оказалось, что не работает)
for eps in [0.5, 1.0, 1.5]:
    for min_samples in [3, 4, 5]:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels_dbscan = dbscan.fit_predict(X_scaled)
        results.append(evaluate_clustering(f"DBSCAN (eps={eps}, min_samples={min_samples})", labels_dbscan, X_scaled, y_true))

# 7. Spectral Clustering
# попробуем разное число соседей
for n_neighbors in [5, 10, 15]:
    spectral = SpectralClustering(n_clusters=3, n_neighbors=n_neighbors, affinity='nearest_neighbors', random_state=42)
    labels_spectral = spectral.fit_predict(X_scaled)
    results.append(evaluate_clustering(f"Spectral (n_neighbors={n_neighbors})", labels_spectral, X_scaled, y_true))

# 8. Gaussian Mixture Models
# попробуем ковариационные матрицы разной формы
for covariance_type in ['full', 'tied', 'diag', 'spherical']:
    gmm = GaussianMixture(n_components=3, covariance_type=covariance_type, random_state=42)
    labels_gmm = gmm.fit_predict(X_scaled)
    results.append(evaluate_clustering(f"GMM (covariance={covariance_type})", labels_gmm, X_scaled, y_true))

# Создание единой таблицы результатов
results_df = pd.DataFrame(results)

# 9. Вывод результатов экспериментов
for method in ["K-Means", "Agglomerative", "DBSCAN", "Spectral", "GMM"]:
    method_results = results_df[results_df["Model"].str.startswith(method)]
    print(f"\nРезультаты {method}:")
    print(method_results.to_string(index=False))

# Выбор лучших моделей
final_results = results_df.groupby(results_df["Model"].str.split().str[0]).apply(select_best_model).reset_index(drop=True)

# Сортировка финальной таблицы по ARI, затем Silhouette
final_results = final_results.sort_values(by=["ARI", "Silhouette"], ascending=[False, False])

# Вывод финальной таблицы
print("\nЛучшие модели по каждому методу (отсортированы по ARI, затем Silhouette):")
print(final_results.to_string(index=False))

# Визуализация лучшей модели
#  нет времени на борьбу с elif'ами
best_model_name = final_results.iloc[0]["Model"]
if "K-Means" in best_model_name:
    best_k = int(best_model_name.split('=')[1][0])
    best_model = KMeans(n_clusters=best_k, random_state=42).fit(X_scaled)
    best_labels = best_model.labels_
elif "Agglomerative" in best_model_name:
    linkage = best_model_name.split('=')[1][:-1]
    best_model = AgglomerativeClustering(n_clusters=3, linkage=linkage).fit(X_scaled)
    best_labels = best_model.labels_
elif "DBSCAN" in best_model_name:
    eps = float(best_model_name.split('=')[1].split(',')[0])
    min_samples = int(best_model_name.split('=')[2][:-1])
    best_model = DBSCAN(eps=eps, min_samples=min_samples).fit(X_scaled)
    best_labels = best_model.labels_
elif "Spectral" in best_model_name:
    n_neighbors = int(best_model_name.split('=')[1][:-1])
    best_model = SpectralClustering(n_clusters=3, n_neighbors=n_neighbors, affinity='nearest_neighbors', random_state=42).fit(X_scaled)
    best_labels = best_model.labels_
elif "GMM" in best_model_name:
    covariance_type = best_model_name.split('=')[1][:-1]
    best_model = GaussianMixture(n_components=3, covariance_type=covariance_type, random_state=42).fit(X_scaled)
    best_labels = best_model.predict(X_scaled)  # Используем predict для GMM

# Визуализируем результат
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=best_labels, cmap='viridis', s=50)
plt.title(f"Результат кластеризации: {best_model_name}")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.show()

'''
Вывод программы.
Результаты K-Means:
        Model  Silhouette  DB Index   ARI   NMI
K-Means (k=2)       0.265     1.494 0.367 0.479
K-Means (k=3)       0.285     1.389 0.897 0.876
K-Means (k=4)       0.254     1.695 0.817 0.798
Результаты Agglomerative:
                           Model  Silhouette  DB Index    ARI   NMI
    Agglomerative (linkage=ward)       0.277     1.419  0.790 0.786
Agglomerative (linkage=complete)       0.204     1.896  0.577 0.614
 Agglomerative (linkage=average)       0.158     1.030 -0.005 0.018
  Agglomerative (linkage=single)       0.183     0.911 -0.007 0.035
Результаты DBSCAN:
                          Model  Silhouette  DB Index  ARI   NMI
DBSCAN (eps=0.5, min_samples=3)         NaN       NaN 0.00 0.000
DBSCAN (eps=0.5, min_samples=4)         NaN       NaN 0.00 0.000
DBSCAN (eps=0.5, min_samples=5)         NaN       NaN 0.00 0.000
DBSCAN (eps=1.0, min_samples=3)         NaN       NaN 0.00 0.000
DBSCAN (eps=1.0, min_samples=4)         NaN       NaN 0.00 0.000
DBSCAN (eps=1.0, min_samples=5)         NaN       NaN 0.00 0.000
DBSCAN (eps=1.5, min_samples=3)      -0.277     1.563 0.04 0.216
DBSCAN (eps=1.5, min_samples=4)      -0.072     1.503 0.01 0.089
DBSCAN (eps=1.5, min_samples=5)         NaN       NaN 0.00 0.000
Результаты Spectral:
                    Model  Silhouette  DB Index  ARI   NMI
 Spectral (n_neighbors=5)       0.283     1.394 0.85 0.834
Spectral (n_neighbors=10)       0.283     1.391 0.88 0.861
Spectral (n_neighbors=15)       0.283     1.391 0.88 0.861
Результаты GMM:
                     Model  Silhouette  DB Index   ARI   NMI
     GMM (covariance=full)       0.285     1.389 0.897 0.876
     GMM (covariance=tied)       0.284     1.387 0.913 0.892
     GMM (covariance=diag)       0.281     1.416 0.864 0.847
GMM (covariance=spherical)       0.272     1.407 0.879 0.855
Лучшие модели по каждому методу (отсортированы по ARI, затем Silhouette):
                          Model  Silhouette  DB Index   ARI   NMI
          GMM (covariance=tied)       0.284     1.387 0.913 0.892
                  K-Means (k=3)       0.285     1.389 0.897 0.876
      Spectral (n_neighbors=10)       0.283     1.391 0.880 0.861
   Agglomerative (linkage=ward)       0.277     1.419 0.790 0.786
DBSCAN (eps=1.5, min_samples=3)      -0.277     1.563 0.040 0.216

Выбранные модели.
Исходя из характера датасета, для кластеризации выбраны следующие алгоритмы:
K-Means - универсальный и быстрый алгоритм для компактных кластеров, хорошо работает с числовыми данными,
Agglomerative Clustering - эффективен для изучения иерархических структур данных, позволяет понять внутренние связи между наблюдениями,
DBSCAN - подходит для выявления плотностных кластеров и автоматической идентификации выбросов,
Spectral Clustering - способен находить сложные структуры кластеров,
GMM - использует вероятностный подход для нахождения перекрывающихся кластеров.

Выбранные метрики.
Для кластеризации будем использовать две группы метрик.
Внутренние метрики (без учета y):
Silhouette Score - оценивает компактность и разделимость кластеров (чем выше, тем лучше),
Davies-Bouldin Index (DBI) - чем ниже индекс, тем лучше.
Внутренние метрики позволяют понять, насколько хорошо алгоритм разбивает данные, даже если истинные метки нам неизвестны.
 Внешние метрики (с учетом y).
Эти метрики сравнивают результаты кластеризации с реальными метками:
Adjusted Rand Index (ARI) - измеряет схожесть кластеров с истинными метками, учитывая случайные совпадения,
Normalized Mutual Information (NMI) - показывает, сколько информации о реальных метках содержится в кластерах.
Внешние метрики показывают, насколько хорошо кластеры совпадают с исходной классификацией.

Выбранный алгоритм.
1. Gaussian Mixture Models (GMM) - победитель.
лучшая модель: GMM (covariance=tied), которая получила ARI = 0.913 и Silhouette = 0.284.
2. K-Means - тоже чемпион.
лучшая модель: K-Means (k=3) с ARI = 0.897 и Silhouette = 0.285.
3. Spectral Clustering - третье место.
лучшая модель: Spectral (n_neighbors=10) с ARI = 0.880 и Silhouette = 0.283.
4. Agglomerative Clustering - вряд ли подойдет.
лучшая модель: Agglomerative (linkage=ward) с ARI = 0.790 и Silhouette = 0.277.
5. DBSCAN - не годится.
'''

