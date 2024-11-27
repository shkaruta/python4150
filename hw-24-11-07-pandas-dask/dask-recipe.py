# Работа с большими данными и библиотекой dask
# В архиве хранятся 8 csv-файлов с рецептами общим объемом 1,2 млн записей
# Пример использования dask, zipfile, csv, sqlite

import zipfile
import dask.dataframe as dd

# 1. Распаковка архива и загрузка всех CSV-файлов
zipfilename = 'recipes_full.zip'
with zipfile.ZipFile(zipfilename, "r") as archive:
    archive.extractall()  

# Список всех CSV-файлов в распакованном каталоге
csv_files = [f for f in archive.namelist() if f.endswith('.csv')]
print("Файлы в архиве:", ', '.join(csv_files))

# Загрузка файлов с использованием Dask
# Dask позволяет работать с большими объемами данных за счёт ленивой загрузки и обработки
# читаем с параметром assume_missing=True, чтобы нивелировать ошибки типа данных в проблемных ячейках
df = dd.read_csv(csv_files, assume_missing=True)

# 2. Вывод метаинформации о таблице
print("Датафрейм dask загружен")
print(f"Количество разделов (npartitions): {df.npartitions}")
print("Типы столбцов:")
print(df.dtypes)

# 3. Вывод первых 5 строк таблицы
# .head() загружает в память только 5 первых строк
print('-'*16)
print("Первые 5 строк:")
print(df.head())

# 4. Вывод последних 5 строк таблицы
# .tail() также загружает в память только последние 5 строк
print('-'*16)
print("Последние 5 строк:")
print(df.tail())

# 5. Подсчёт количества строк в каждом разделе
# Dask разбивает данные на разделы (partitions) для обработки
print('-'*16)
print("Количество строк в каждом разделе:")
rows_per_partition = df.map_partitions(len).compute()  
print(rows_per_partition)

# 6. Поиск максимума в столбце n_steps
max_steps = df['n_steps'].max()
print('-'*16)
print(f"Максимум в столбце n_steps: {max_steps.compute()}")
# Выводим граф вычислений, объяснение в конце этого файла
print("Граф вычислений максимума в столбце n_steps в текстовом виде")
# Преобразуем граф в текст с разделением по строкам
graph_text = str(max_steps.dask)
print('\n'.join(graph_text.split(',')))

# 7. Группировка по месяцам добавления отзывов
# Преобразуем 'submitted' в datetime для работы с датами
df['submitted'] = dd.to_datetime(df['submitted'], format='%Y-%m-%d', errors='coerce')
# Группируем данные по году и месяцу и считаем количество записей
grouped = df.groupby(df['submitted'].dt.to_period('M')).size()
# Вычисляем результат, сортируя его по индексу
result = grouped.compute().sort_index()
print('-'*16)
print("Количество отзывов по месяцам:")
print(result)

# 8. Поиск пользователя, отправлявшего рецепты чаще всего
top_contributor = df['contributor_id'].value_counts().idxmax().compute()
# Количество рецептов для этого пользователя
top_contributor_count = df['contributor_id'].value_counts().max().compute()
print('-'*16)
print(f"Пользователь, отправлявший рецепты чаще всего: ID = {top_contributor}")
print(f"Количество рецептов: {top_contributor_count}")

# 9. Самый первый и самый последний рецепт по дате
first_recipe = df[df['submitted'] == df['submitted'].min()].compute()
last_recipe = df[df['submitted'] == df['submitted'].max()].compute()
print('-'*16)
print("Первый по дате рецепт:")
print(first_recipe)
print("Последний по дате рецепт:")
print(last_recipe)
# Если дат с минимумом или максимумом несколько, все они будут отображены.

# 10. Загрузка данных в SQLite
sqlite_filename = 'recipes.db'
# Создаем строку подключения, тройной слеш - для локального файла
sqlite_uri = f'sqlite:///{sqlite_filename}'
# Загружаем данные из Dask DataFrame в базу данных SQLite
df.to_sql('recipes', sqlite_uri, if_exists='replace', index=False, compute=True)
print('-'*16)
print(f"Данные успешно загружены в базу SQLite: {sqlite_filename}")

# 11. Отбор рецептов и сохранение в CSV
filtered_recipes_filename = 'filtered_recipes.csv'
# Вычисляем медиану для времени приготовления (0.5 квантиль) (в даске нет медианы)
median_minutes = df['minutes'].quantile(0.5).compute()
print('-'*16)
print("Медиана времени приготовления:", median_minutes)
# Вычисляем среднее количество шагов
mean_steps = df['n_steps'].mean().compute()
print("Среднее количество шагов:", mean_steps)
# Отбираем рецепты, где время приготовления < медианы и количество шагов < среднего
filtered_recipes = df[(df['minutes'] < median_minutes) & (df['n_steps'] < mean_steps)]
# Сохраняем отфильтрованные данные в CSV
filtered_recipes.compute().to_csv(filtered_recipes_filename, index=False)
print(f"Отфильтрованные рецепты успешно сохранены в файл {filtered_recipes_filename}")

'''
Объяснение графа вычислений

1. Граф вычислений — это структура, которая:
1) отображает последовательность операций и взаимосвязь между ними
2) состоит из узлов (операции или данные) и ребер (зависимости)
3) используется Dask для оптимизации вычислений, распределяя задачи по ядрам процессора или узлам кластера
Граф вычислений в Dask генерируется лениво: вычисления выполняются только тогда, когда вызывается метод .compute().

2. Как работает Dask в этом случае.
2.1. Чтение данных из файлов:
dask делит исходные CSV-файлы на более мелкие части (разделы), которые обрабатываются независимо
каждый раздел содержит информацию о столбце n_steps
2.2. Распределение задач:
dask создает задачи для поиска локального максимума в каждом разделе
эти задачи выполняются параллельно
2.3. Агрегация результатов:
после получения локальных максимумов Dask находит глобальный максимум, объединяя результаты

3. Вывод графа вычислений.
Для вывода можно воспользоваться vizualize, но для этого нужно устанавливать graphviz.
А можно сделать вывод в текстовом виде:
print(max_steps.dask)
Для вывода разных шагов вычислений на разных строках можно воспользоваться pprint или разобрать структуру вручную.
'''
'''
Вывод программы.
Файлы в архиве: recipes_full/recipes_full_0.csv, recipes_full/recipes_full_1.csv, recipes_full/recipes_full_2.csv, recipes_full/recipes_full_3.csv, recipes_full/recipes_full_4.csv, recipes_full/recipes_full_5.csv, recipes_full/recipes_full_6.csv, recipes_full/recipes_full_7.csv
Датафрейм dask загружен
Количество разделов (npartitions): 16
Типы столбцов:
id                        float64
name              string[pyarrow]
minutes                   float64
contributor_id            float64
submitted         string[pyarrow]
n_steps                   float64
description       string[pyarrow]
n_ingredients             float64
dtype: object
----------------
Первые 5 строк:
          id                                               name  minutes  contributor_id   submitted  n_steps                                        description  n_ingredients
0   683970.0                        vant ivoire mickies nothing     33.0        803776.0  2019-08-22      4.0  pat and gina neely and their family own and op...            9.0
1  1089012.0  kremsils mariposa baccala cookies class borage...     23.0         51579.0  2013-03-02      1.0  a light, tasty and easy to put together chicke...            5.0
2  1428572.0                                       tania lander      0.0         68884.0  1980-11-09      1.0  a delicious melt in your mouth appetizer. for ...            5.0
3  1400250.0                heloise milli asher doogh zojirushi     24.0        678862.0  2018-04-29      3.0  delicious cream cheese and peach filled cresce...            1.0
4   387709.0                      nutty chocolate chunk cookies     47.0        489552.0  2009-08-31      8.0  everyone loves these buttery cookies chock ful...           10.0
----------------
Последние 5 строк:
               id                                         name  minutes  contributor_id   submitted  n_steps                                        description  n_ingredients
139587  1029131.0              tuti waffle snackies steakhouse     19.0        171345.0  1973-10-18      4.0  according to a providence journal article, ama...            4.0
139588  1700703.0    noelias cheats crocante fleisch zitumbuwa      1.0         30228.0  2007-07-01      6.0  if possible sauté the onions and garlic in abo...            1.0
139589  1910650.0  rubbed restuffed pelmeni bedouin flavourful     60.0        591905.0  2009-09-26      3.0  another great recipe to add to the growing swe...            2.0
139590   713836.0                       stems polpettine peezi      NaN        357389.0  2003-09-30      4.0        adapted from top secret recipes. love this!            9.0
139591   660699.0                                  clementines     64.0         29196.0  1973-06-03      6.0  this would make a great start to your holiday ...            8.0
----------------
Количество строк в каждом разделе:
0     139475
1     139480
2     139577
3     139378
4     139502
5     139453
6     139619
7     139336
8     139687
9     139268
10    139423
11    139531
12    139574
13    139380
14    139362
15    139592
dtype: int64
----------------
Максимум в столбце n_steps: 145.0
Граф вычислений максимума в столбце n_steps в текстовом виде
{('max-tree-5a170e081d7918d672bf11cd7944393a'
 0): (<function apply at 0x0000025727800180>
 <bound method Reduction.aggregate of <class 'dask_expr._reductions.Max'>>
 [[('chunk-429113a82ce6c46c90769ba5ff581109'
 0)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 1)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 2)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 3)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 4)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 5)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 6)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 7)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 8)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 9)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 10)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 11)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 12)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 13)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 14)
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 15)]]
 {'skipna': True
 'axis': 0})
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 0): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 0) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 1): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 1) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 2): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 2) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 3): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 3) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 4): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 4) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 5): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 5) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 6): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 6) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 7): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 7) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 8): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 8) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 9): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 9) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 10): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 10) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 11): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 11) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 12): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 12) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 13): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 13) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 14): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 14) chunk(...
 ...)>
 ('chunk-429113a82ce6c46c90769ba5ff581109'
 15): <Task ('chunk-429113a82ce6c46c90769ba5ff581109'
 15) chunk(...
 ...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 0): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 0) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 1): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 1) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 2): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 2) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 3): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 3) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 4): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 4) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 5): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 5) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 6): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 6) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 7): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 7) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 8): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 8) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 9): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 9) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 10): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 10) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 11): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 11) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 12): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 12) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 13): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 13) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 14): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 14) getitem(...)>
 ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 15): <Task ('getitem-8f1f488c4f678ca7a0088a4a49f941a2'
 15) getitem(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 0): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 0) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 1): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 1) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 2): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 2) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 3): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 3) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 4): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 4) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 5): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 5) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 6): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 6) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 7): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 7) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 8): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 8) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 9): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 9) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 10): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 10) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 11): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 11) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 12): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 12) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 13): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 13) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 14): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 14) lambda(...)>
 ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 15): <Task ('read_csv-255b433c545b4050feddecbb16bcf5b2'
 15) lambda(...)>}
----------------
Количество отзывов по месяцам:
submitted
1970-01    3306
1970-02    2943
1970-03    3324
1970-04    3245
1970-05    3284
           ...
2021-04    3139
2021-05    3223
2021-06    3128
2021-07    3342
2021-08    1195
Freq: M, Length: 620, dtype: int64
----------------
Пользователь, отправлявший рецепты чаще всего: ID = 89831.0
Количество рецептов: 30105
----------------
Первый по дате рецепт:
               id                                               name  minutes  contributor_id  submitted  n_steps                                        description  n_ingredients
4700    1460605.0  cobs pannbiff tuned camaroes saharan three ara...     42.0        305531.0 1970-01-01      2.0  that actually does not taste low fat, true!not...            4.0
36059    753293.0  dis spa senapsgrdde kartoffelsalat fassoula hilde      8.0        518108.0 1970-01-01      5.0                                  fabulous recipe!!            2.0
46736   1798761.0                     rivvels spepper rigati fireman     48.0         29431.0 1970-01-01      4.0  try these with my baked bean recipe. the combi...            4.0
87958   1377272.0                                           panfired     60.0         89831.0 1970-01-01      6.0  a wonderful greek inspired salad. makes a grea...            6.0
98297   2022227.0  hogan kayisi liptauer interchangable mickeys s...     27.0         21752.0 1970-01-01      1.0  i found this recipe in an issue of everyday fo...            2.0
...           ...                                                ...      ...             ...        ...      ...                                                ...            ...
10678   1971296.0  points donofrio cynna smoothie kheema brandon ...     21.0        480195.0 1970-01-01      4.0                               from drinkmixer.com.            8.0
42565   2190993.0  decoration charley leuang petoules she mmm bct...     39.0       1142997.0 1970-01-01      2.0  wonderful creamy chicken without heating up th...            1.0
50146   1158091.0  chippers pointe calf nigel bloemkool tesco che...     14.0       1105991.0 1970-01-01      5.0                                                NaN            9.0
59872    896167.0                                          kohlsuppe     45.0        552613.0 1970-01-01      4.0  plan ahead the chicken strips need to chill fo...            5.0
121703   281710.0               strict toby stovies yenkukhu quarter     12.0        687956.0 1970-01-01      5.0  my mom made this for us all the time when we w...            3.0
[110 rows x 8 columns]
Последний по дате рецепт:
               id                                               name  minutes  contributor_id  submitted  n_steps                                        description  n_ingredients
89909   1381565.0       lovin quesadillos hpnotiq macrobiotic reader     52.0          6810.0 2021-08-12      5.0  the best nachos ever. exactly like taco bell x...            5.0
124595   448274.0                                            impress      0.0        136997.0 2021-08-12      6.0  sweet from the onions, creamy and rich tasting...            7.0
46203   1494057.0              milho crusher josy schweinskoteletten     35.0       1305870.0 2021-08-12      5.0  this is a sephardic meat stew that is enjoyed ...            5.0
50447   1759085.0                                         palocleves     40.0         42340.0 2021-08-12      3.0  love these stewed tomatoes better than the one...            9.0
84407   2141033.0                                             smudgy      5.0        258867.0 2021-08-12      3.0                     for baby back ribs; delicious.            8.0
...           ...                                                ...      ...             ...        ...      ...                                                ...            ...
57810    497607.0                                      about lorilou     16.0        171084.0 2021-08-12      3.0  this is an old family recipe. we cooked it wit...            9.0
73067   1767902.0                                      konijn brocco     57.0        949208.0 2021-08-12      6.0  another fabulous recipe from www.meals.com. us...            6.0
115236  2205491.0                                          casserole     19.0        506822.0 2021-08-12      6.0  i know the title seems somewhat bizarre, but t...            8.0
116977  1324555.0  dulcet parmburgers fairfield moule greenfield ...      5.0         47892.0 2021-08-12      6.0  this recipe was adapted from another cooking w...            9.0
133085   623588.0  1933 japanese wolfensburger chess lacis bourek...     59.0        567111.0 2021-08-12      5.0  something i found in a magazine. 14 april, 200...            2.0
[79 rows x 8 columns]
----------------
Данные успешно загружены в базу SQLite: recipes.db
----------------
Медиана времени приготовления: 33.0
Среднее количество шагов: 4.151083263093415
Отфильтрованные рецепты успешно сохранены в файл filtered_recipes.csv
'''
