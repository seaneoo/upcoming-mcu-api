import itertools
from typing import List, Tuple

import certifi
import httpx
import motor.motor_asyncio
from pymongo.collection import Collection

from app.models.v1 import Production
from config import config
from database.v1.models import Movie, Series

_connection_uri = config['MONGO_CONNECTION_URI']
_tmdb_url = 'https://api.themoviedb.org/3/'
_tmdb_token = config['TMDB_TOKEN']
_tmdb_list = '8254729'

db_client = motor.motor_asyncio.AsyncIOMotorClient(
    _connection_uri, tlsCAFile=certifi.where())
database = db_client['upcomingmcu']
collection: Collection = database['productions']


def fetch(path: str) -> httpx.Response:
    with httpx.Client() as client:
        try:
            r = client.get(_tmdb_url + path,
                           headers={'authorization': f'Bearer {_tmdb_token}'})
            r.raise_for_status()
            return r
        except httpx.HTTPStatusError as e:
            print(
                f'Code {e.response.status_code} while requesting {e.request.url}')


def wipe():
    collection.delete_many({})


def insert(item):
    collection.insert_one(item)


def productions_from_list() -> List[Tuple[int, str]]:
    productions = []
    r = fetch(f'list/{_tmdb_list}')
    if r:
        items = r.json()['items']
        productions = [(item['id'], item['media_type']) for item in items]
    return productions


def get_movie(movie_id: int):
    r = fetch(f'movie/{movie_id}')
    data: Movie = r.json()
    return data


def get_series(series_id: int):
    r = fetch(f'tv/{series_id}')
    data: Series = r.json()
    return data


def parse_movie(item: Movie) -> Production:
    return {
        'id': item['id'],
        'title': item['title'],
        'overview': item['overview'],
        'release_date': item['release_date'],
        'type': 'movie',
        'poster': item['poster_path']
    }


def parse_series(item: Series) -> list[Production]:
    productions: list[Production] = []
    for season in item['seasons']:
        productions.append({
            'id': item['id'],
            'title': f'{item["name"]} Season {season["season_number"]}' if item['number_of_seasons'] > 1 else item['name'],
            'overview': season['overview'],
            'release_date': season['air_date'],
            'type': 'tv',
            'poster': season['poster_path']
        })
    return productions


def parse_production(item: Movie | Series, media_type: str) -> list[Production]:
    productions: list[Production] = []
    if media_type == 'movie':
        productions.append(parse_movie(item))
    elif media_type == 'tv':
        productions.extend(parse_series(item))
    return productions


def build_all():
    wipe()

    productions = productions_from_list()
    for (id, media_type) in productions:
        item: Movie | Series = None

        match media_type:
            case 'movie': item = get_movie(id)
            case 'tv': item = get_series(id)

        parsed_productions = parse_production(item, media_type)
        for pp in parsed_productions:
            insert(pp)
