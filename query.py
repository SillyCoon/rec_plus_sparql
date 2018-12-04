import json

from SPARQLWrapper import SPARQLWrapper, JSON
from requests import get


def getFilmUri(movie_title: str):
    json = get('https://www.wikidata.org/w/api.php', {
        'action': 'wbgetentities',
        'titles': movie_title,
        'sites': 'enwiki',
        'props': '',
        'format': 'json'
    }).json()
    filmUri = list(json['entities'])[0]
    return filmUri


def film_query(filmName):
    filmUri = getFilmUri(filmName)

    sparql = SPARQLWrapper("http://query.wikidata.org/sparql")
    sparql.setQuery("""
    SELECT DISTINCT ?film ?filmLabel ?myear WHERE {
      # Находим год выбранного фильма
      wd:%s wdt:P577 ?mydate.
      BIND (str(YEAR(?mydate)) as ?myear).
      
      # Находим год всех фильмов
      ?film wdt:P31 wd:Q11424.
      ?film wdt:P577 ?date.
      
      # Выбираем наш фильм и фильмы с тем же годом выхода
      FILTER(YEAR(?date) = YEAR(?mydate))
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """ % filmUri)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


