## Задание 6
'''
Дана большая строка, например
s = "Мистер и миссис Дурсль проживали в доме номер четыре по Тисовой улице и всегда с гордостью заявляли, что они, слава богу, абсолютно нормальные люди. Уж от кого-кого, а от них никак нельзя было ожидать, чтобы они попали в какую-нибудь странную или загадочную ситуацию. Мистер и миссис Дурсль весьма неодобрительно относились к любым странностям, загадкам и прочей ерунде."
* приведите все слова в строке к нижнему регистру
* очистите строку от знаков припенания
* создайте из строки список слов
* создайте словарь, где ключем будет слово, а значение - сколько раз оно встретилось в строке. Отсортируйте словарь в порядке убывания встречаемости слов.
'''
from string import punctuation
s = "Мистер и миссис Дурсль проживали в доме номер четыре по Тисовой улице и всегда с гордостью заявляли, что они, слава богу, абсолютно нормальные люди. Уж от кого-кого, а от них никак нельзя было ожидать, чтобы они попали в какую-нибудь странную или загадочную ситуацию. Мистер и миссис Дурсль весьма неодобрительно относились к любым странностям, загадкам и прочей ерунде."
s_wo_punctuation = ''.join(c for c in s if c not in punctuation.replace('-',''))
s_list = s_wo_punctuation.split()
dct = {}
for word in s_list:
    dct[word] = dct.get(word, 0) + 1
print(f'Original string: {s}\n'+
    f'Lowercase: {s.lower()}\n'+
    f'W/o punctuation: {s_wo_punctuation}\n'+
    f'Word list: {s_list}\n'+
    f'Sorted dict: {dict(sorted(dct.items(), key = lambda x: -x[1]))}')