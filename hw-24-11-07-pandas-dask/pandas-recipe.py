# Работа с csv-файлом кулинарных рецептов объемом 280000 записей
# Пример использования pandas, zipfile, sqlalchemy, sqlite
import zipfile  
import pandas as pd  
from sqlalchemy import create_engine  

# 1. Распаковка архива recipes_full.zip в текущую папку
zipfilename = 'recipes_full.zip'
with zipfile.ZipFile(zipfilename, "r") as archive:
    archive.extractall()  
# Проверим, какие файлы были извлечены
extracted_files = archive.namelist()  
print("Файлы в архиве:", ', '.join(extracted_files))

# 2. Считывание первого файла из архива
# под индексом 0 в данном случае имя каталога, поэтому первый файл будет с индексом 1
file_name = extracted_files[1]
data = pd.read_csv(file_name, delimiter=',')

# Проверка типов данных и отображение первых строк для верификации
print("-"*16)
print("Типы данных в файле")
print(data.dtypes)
print("-"*16)
print("Заголовки и первые 3 строки")
print(data.head(3))

# 3. Нахождение максимума в столбце n_steps
max_steps = data["n_steps"].max()
print("-"*16)
print("Максимальное количество шагов:", max_steps)

# 4. Количество отзывов, сгруппированное по месяцам добавления
# преобразуем столбец `submitted` из строкового (здесь object) в формат datetime
# при помощи функции pd.to_datetime
# data["submitted"] = pd.to_datetime(data["submitted"], format="%Y-%m-%d")
data["submitted"] = pd.to_datetime(data["submitted"], format="%Y-%m-%d", errors="coerce")

# группируем по месяцам
# метод .dt.to_period("M") извлекает год и месяц из объекта datetime
reviews_by_month = data.groupby(data["submitted"].dt.to_period("M")).size()

print("-"*16)
print("Количество отзывов, сгруппированное по месяцам:")
print(reviews_by_month)
# Если pandas выводит длинный список, он автоматически сокращает его для удобства, показывая только первые и последние строки, а остальное заменяет многоточием
# Чтобы вывести все строки, нужно указать .to_string())
# print(reviews_by_month.to_string())

# 5. Пользователь, отправлявший рецепты чаще всего
top_contributor = data["contributor_id"].value_counts().idxmax()
print("-"*16)
print("Самый активный пользователь:", top_contributor)

# 6. Самый первый и самый последний по дате рецепт
first_recipe = data.loc[data["submitted"].idxmin()]
last_recipe = data.loc[data["submitted"].idxmax()]
print("-"*16)
print("Первый рецепт:")
print(first_recipe)
print("-"*16)
print("Последний рецепт:")
print(last_recipe)

# 7. Медианы по количеству ингредиентов и времени приготовления
median_ingredients = data["n_ingredients"].median()
median_time = data["minutes"].median()
print("-"*16)
print("Медиана по ингредиентам:", median_ingredients)
print("Медиана по времени приготовления:", median_time)

# 8. Самый простой рецепт по условиям
simplest_recipe = data.sort_values(
    by=["n_ingredients", "minutes", "n_steps"]
).iloc[0]
print("-"*16)
print("Самый простой рецепт:")
print(simplest_recipe)

# 9. Загрузка рецептов в базу данных SQLite
# тройной слэш /// — стандартный синтаксис для указания локального файла SQLite в URI
sqlite_filename = 'recipes.db'
table_name = 'recipes'
engine = create_engine(f"sqlite:///{sqlite_filename}")
# Сохраняем данные в таблицу table_name
data.to_sql(table_name, engine, if_exists="replace", index=False)
print("-"*16)
print(f"Рецепты загружены в таблицу {table_name} базы данных {sqlite_filename}")

# 10. Отбор рецептов с временем приготовления меньше медианы и количеством шагов меньше среднего
filtered_filename = 'filtered_recipes.csv'
mean_steps = data["n_steps"].mean()
filtered_recipes = data[
    (data["minutes"] < median_time) & (data["n_steps"] < mean_steps)
]
filtered_recipes.to_csv(filtered_filename, index=False)
print("-"*16)
print("Рецепты с малым временем приготовления и количеством шагов отобраны и сохранены в файл", filtered_filename)


'''
Вывод результатов
Файлы в архиве: recipes_full/, recipes_full/recipes_full_0.csv, recipes_full/recipes_full_1.csv, recipes_full/recipes_full_2.csv, recipes_full/recipes_full_3.csv, recipes_full/recipes_full_4.csv, recipes_full/recipes_full_5.csv, recipes_full/recipes_full_6.csv, 
recipes_full/recipes_full_7.csv
----------------
Типы данных в файле
id                 int64
name              object
minutes            int64
contributor_id     int64
submitted         object
n_steps            int64
description       object
n_ingredients      int64
dtype: object
----------------
Заголовки и первые 3 строки
        id                                               name  minutes  contributor_id   submitted  n_steps                                        description  n_ingredients
0   683970                        vant ivoire mickies nothing       33          803776  2019-08-22        4  pat and gina neely and their family own and op...              9
1  1089012  kremsils mariposa baccala cookies class borage...       23           51579  2013-03-02        1  a light, tasty and easy to put together chicke...              5
2  1428572                                       tania lander        0           68884  1980-11-09        1  a delicious melt in your mouth appetizer. for ...              5
----------------
Максимальное количество шагов: 110
----------------
Количество отзывов, сгруппированное по месяцам:
submitted
1970-01    389
1970-02    382
1970-03    422
1970-04    374
1970-05    408
          ...
2021-04    393
2021-05    413
2021-06    363
2021-07    449
2021-08    149
Freq: M, Length: 620, dtype: int64
----------------
Самый активный пользователь: 89831
----------------
Первый рецепт:
id                                                          1460605
name              cobs pannbiff tuned camaroes saharan three ara...
minutes                                                          42
contributor_id                                               305531
submitted                                       1970-01-01 00:00:00
n_steps                                                           2
description       that actually does not taste low fat, true!not...
n_ingredients                                                     4
Name: 4700, dtype: object
----------------
Последний рецепт:
id                                                          1381565
name                   lovin quesadillos hpnotiq macrobiotic reader
minutes                                                          52
contributor_id                                                 6810
submitted                                       2021-08-12 00:00:00
n_steps                                                           5
description       the best nachos ever. exactly like taco bell x...
n_ingredients                                                     5
Name: 89909, dtype: object
----------------
Медиана по ингредиентам: 5.0
Медиана по времени приготовления: 33.0
----------------
Самый простой рецепт:
id                                                          2182351
name              tandoor knackwurst pagac suprises expressive v...
minutes                                                           0
contributor_id                                                23102
submitted                                       1980-06-13 00:00:00
n_steps                                                           1
description       chocolate and orange is one of my favourite co...
n_ingredients                                                     1
Name: 9330, dtype: object
----------------
Рецепты загружены в таблицу recipes базы данных recipes.db
----------------
Рецепты с малым временем приготовления и количеством шагов отобраны и сохранены в файл filtered_recipes.csv

'''
