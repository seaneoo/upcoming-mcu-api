from typing import List, TypedDict


class Movie(TypedDict):
    id: int
    overview: str
    poster_path: str
    release_date: str
    title: str


class Season(TypedDict):
    air_date: str
    id: int
    name: str
    overview: str
    poster_path: str
    season_number: int


class Series(TypedDict):
    id: int
    name: str
    overview: str
    poster_path: str
    number_of_seasons: int
    seasons: List[Season]


class Production(TypedDict):
    id: str
    title: str
    overview: str
    release_date: str
    type: str
    poster: str
