from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Production(BaseModel):
    id: str = Field(default=None)
    title: str = Field(default=None)
    overview: str = Field(default=None)
    release_date: str = Field(default=None)
    type: str = Field(default=None)
    poster: str = Field(default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "299534",
                "title": "Avengers: Endgame",
                "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos' actions and restore order to the universe once and for all, no matter what consequences may be in store.",
                "release_date": "2019-04-24",
                "type": "movie",
                "poster": "/or06FN3Dka5tukK1e9sl16pB3iy.jpg"
            }
        }


class ProductionResults(BaseModel):
    count: int = Field(default=0)
    results: List[Production] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "count": 2,
                "results": [{
                    "id": "447365",
                    "title": "Guardians of the Galaxy Vol. 3",
                    "overview": "Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own. A mission that, if not completed successfully, could quite possibly lead to the end of the Guardians as we know them.",
                    "release_date": "2023-05-03",
                    "type": "movie",
                    "poster": "/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg"
                }, {
                    "id": "114472",
                    "title": "Secret Invasion",
                    "overview": "Nick Fury and Talos discover a faction of shapeshifting Skrulls who have been infiltrating Earth for years.",
                    "release_date": "2023-06-21",
                    "type": "tv",
                    "poster": "/e6WyanwfUSSEL5LNnm0bWJpYp6J.jpg"
                }]
            }
        }
