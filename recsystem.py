import csv
import math
import datetime

# Открываем файл csv с данными по оценкам фильмов и записываем его в список
with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    marks = list(reader)

# Лямбда выражение для корректного приведения строкового типа к int
to_int = lambda a: (int)(a.replace('\n', ''))

# Приведения оценок к типу int
for i in range(1, len(marks)):
    for j in range(1, len(marks[0])):
        marks[i][j] = to_int(marks[i][j])

# Обработка пользователя под номером 16 согласно заданию
u = 16


# Функция определяет насколько пользователи похожи во вкусах
# На вход подаются номера пользователей
def Similarity(u, v):
    global marks
    # Вспомогательные переменные для расчёта формулы
    simUV = 0
    simU = 0
    simV = 0
    # Количество фильмов
    m = len(marks[0])
    for i in range(1, m):
        # Разбираем только просмотренные фильмы нашим пользователем и остальными
        if (marks[u][i] != -1) and (marks[v][i] != -1):
            simUV = simUV + (marks[u][i] * marks[v][i])
            simU = simU + (marks[u][i] ** 2)
            simV = simV + (marks[v][i] ** 2)

    total = simUV / (math.sqrt(simU) * math.sqrt(simV))
    return total


# Функция для расчёта средней оценки пользователя
def getMiddle(mid):
    global marks
    # Составляем список оценок пользователя, не включая в него непросмотренные фильмы
    mid_lst = [marks[mid][i] for i in range(1, len(marks[0])) if marks[mid][i] != -1]

    return sum(mid_lst) / len(mid_lst)


# Расчёт предполагаемой оценки пользователя
def getRecomendationMark(u, film, simList):
    global marks
    # Среднее значение оценок пользователя
    midRu = getMiddle(u)
    # Вспомогательные переменные для расчёта
    sumRv = 0
    sumSim = 0
    for key in simList:
        if (marks[key[0]][film] != -1):
            sumRv = sumRv + (key[1] * (marks[key[0]][film] - getMiddle(key[0])))
            sumSim = sumSim + math.fabs(key[1])
    if (sumSim != 0):
        return midRu + (sumRv / sumSim)
    else:
        return 0


# Словарь, составленый из номеров пользователей и коэффициентов их схожести
simDict = {c: Similarity(u, c) for c in range(1, len(marks)) if u != c}

# Отсортированный список с номером пользователя и коэффициентом схожести
l = lambda x: x[1]
simList = sorted(simDict.items(), key=l, reverse=True)[:5]
print("Отсортированный список 5-и похожих пользователей:\n", simList, "\n")

# Список непросмотренных фильмов
listWatchLess = [i for i in range(1, len(marks[0])) if marks[u][i] == -1]
print("Cписок непросмотренных фильмов:\n", listWatchLess, "\n")

# Формирование списка фильмов с предполагаемыми оценками
recFilms = [(key, getRecomendationMark(u, key, simList)) for key in listWatchLess]
print("Список фильмов с рекомендательными оценками: \n", recFilms, "\n")


# Функция определения дня недели по образцу context.csv
def get_day_description(day):
    return {
        day == 0: ' Mon',
        day == 1: ' Tue',
        day == 2: ' Wed',
        day == 3: ' Thu',
        day == 4: ' Fri',
        day == 5: ' Sat',
        day == 6: ' Sun'
    }[True]


# Определяем день, в который пользователь совершает запрос на рекомендацию
day = get_day_description(datetime.datetime.today().weekday())

# Открываем файл csv с данными по оценкам фильмов и записываем его в список
with open('context.csv', 'r') as f:
    reader = csv.reader(f)
    context = list(reader)


# Функция на вход получает список с полученной выборкой по фильмам с их оценками
# Формирует выборку фильмов, предварительные оценки которых превосходят среднюю
def getMiddleMarks(films):
    sumMark = 0
    for i in films:
        sumMark = sumMark + i[1]
    if(sumMark!=0):
        return[i for i in films if i[1] >= (sumMark / len(films))]


# Функция на вход получает список фильмов с оценкой, превосходящей среднюю
# Сравнивает, у какого из фильмов выше оценка просмотра в день недели, совпадающий с днём недели пользователя при совершении запроса
# Выбирается фильм с наибольшим средним рейтингом в данный день
# Если ни один из фильмов не был оценен в данный день, то выбирается больший по оценке
def getMidDayMark(watchList, simList, day):
    global marks
    global context
    total = {}
    for i in watchList:
        sum = 0
        k = 0
        for j in simList:
            print("Movie: ", i[0], "User: ", j[0], "Mark: ", marks[j[0]][i[0]], "Day: ", context[j[0]][i[0]])
            if context[j[0]][i[0]] == day:
                sum = sum + marks[j[0]][i[0]]
                k = k + 1
        else:
            if (sum != 0):
                total[i[0]] = sum / k

    if (total != {}):
        l = lambda x: x[1]
        total_max = sorted(total.items(), key=l, reverse=True)[:1]
        return total_max[0][0]
    else:
        return 0

watchList = getMiddleMarks(recFilms)
print("Список фильмов с оценками, превышающими сренее значение: \n",watchList, "\n")

bestRecomendFilm = getMidDayMark(watchList, simList, day)
if(bestRecomendFilm != 0):
    print("Рекомендуемый фильм:", bestRecomendFilm)
else:
    l = lambda x: x[1]
    total_max = sorted(recFilms, key=l, reverse=True)[:1]
    print("Рекомендуемый фильм:", total_max[0][0])
