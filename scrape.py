import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('api_key')

def get_movie_genres():
    dictionary = {}
    url = "https://api.themoviedb.org/3/genre/movie/list?api_key=" + api_key + "&language=en-US"
    data = requests.get(url).json()
    data = data['genres']
    for genre in data:
        dictionary[genre['id']]  = genre['name']
    return dictionary
def get_tv_genres():
    dictionary = {}
    url = "https://api.themoviedb.org/3/genre/tv/list?api_key=" + api_key + "&language=en-US"
    data = requests.get(url).json()
    data = data['genres']
    for genre in data:
        dictionary[genre['id']]  = genre['name']
    return dictionary

results= {}


URL = "https://www.seattle.gov/filmandmusic/film/film-history"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

tables = soup.find_all("table", class_="table")[:-4]

movie_genres = get_movie_genres()
tv_genres = get_tv_genres()


for table in tables:
    if table is None:
        continue
    head = table.find("thead")

    if head is None:
        year = table.find("tr").find("td").find("h3")
    else:
        year = head.find("tr").find("th")

    year = year.text
    body = table.find("tbody")
    # print(year)
    movies = body.find_all("tr")[1:-1]

    if head is None:
        movies = body.find_all("tr")[2:-1]

    for movie in movies:
        is_movie = True
        title = movie.find_all("td")[0].text
        director = movie.find_all("td")[1].text
        if title == "" or title is None:
            continue

        url = "https://api.themoviedb.org/3/search/movie?api_key=" + api_key + "&language=en-US&query=" + urllib.parse.quote_plus(title) + "&page=1&include_adult=true&year=" + year
        data = requests.get(url).json()
        if (data['total_results'] == 0):
            is_movie = False
            url = "https://api.themoviedb.org/3/search/tv?api_key=" + api_key + "&language=en-US&query=" + urllib.parse.quote_plus(title) + "&page=1&include_adult=true&year=" + year
            data = requests.get(url).json()
            if (data['total_results'] == 0):
                continue
        try:
            # print(data)
            genre_ids = data['results'][0]['genre_ids']
            # print(title + ": " + director)
        except:
            continue

        if len(genre_ids) == 0:
            continue

        for genre_id in genre_ids:
            if is_movie:
                # print(movie_genres[genre_id])
                if movie_genres[genre_id] in results.keys():
                    results[movie_genres[genre_id]]+=1
                else:
                    results[movie_genres[genre_id]]=1
            else:
                # print(tv_genres[genre_id])
                if tv_genres[genre_id] in results.keys():
                    results[tv_genres[genre_id]]+=1
                else:
                    results[tv_genres[genre_id]]=1
    # print()

print(results)
