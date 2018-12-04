import json

import recommendation_class as rcm
import csv
import query

data = []
context_day = []
context_place = []

with open("data/data.csv", "r") as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        data.append(row)

with open("data/context_day.csv", 'r') as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        context_day.append(row)

with open("data/context_place.csv", 'r') as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        context_place.append(row)

data.pop(0)
context_place.pop(0)
context_day.pop(0)

for i in range(0, len(data)):
    data[i].pop(0)
    context_place[i].pop(0)
    context_day[i].pop(0)
    for j in range(0, len(data[0])):
        data[i][j] = data[i][j].lstrip()

recommendation = rcm.Recommendation(data, context_day, context_place)
recommendation.recommend()


# Встраиваем рекомендательную систему
my_user = 13
movie_names = []
for_sparql = recommendation.best_for_one(my_user)

with open('Movie_names.csv', 'r') as dt:
    reader = csv.reader(dt, quoting=csv.QUOTE_ALL)
    for row in reader:
        movie_names.append(row)

best_movie_name = ' '
for name in movie_names:
    if name[0][6:] == str(for_sparql['movie']):
        best_movie_name = name[1]

best_movie_name = best_movie_name.lstrip()

query_result = query.film_query(best_movie_name)

with open("response.json", 'w') as file:
    file.write(json.dumps(query_result["results"]["bindings"], indent=4))
