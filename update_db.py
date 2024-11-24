import requests
from dotenv import load_dotenv

import os


load_dotenv()
token = os.getenv('TOKEN')
headers = {'X-API-KEY': f'{token}'}

# Получение базы фильмов и сохранение списка в db_films.txt
def update_database():
    films_list = []
    for i in range(1, 21):
        response = requests.get(
            'https://api.kinopoisk.dev/v1.4/movie',
            params={
                "page": f"{i}",
                "limit": 50,
                "selectFields": [
                    "name",
                    "id",
                    "poster"
                ],
                "sortField": "id",
                "sortType": 1,
                "lists": "popular-films"
            },
            headers=headers
        )
        movies = response.json()
        films_list.append(movies)

    os.makedirs('data', exist_ok=True)
    with open('data/db_films.txt', 'w') as file:
        for line in films_list:
            file.write(f'{line}\n')