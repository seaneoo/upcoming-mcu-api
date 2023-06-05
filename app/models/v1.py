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
                "overview": "After the devastating events of Avengers: Infinity War...",
                "release_date": "2019-04-26",
                "type": "movie",
                "poster": "or06FN3Dka5tukK1e9sl16pB3iy.jpg",
            }
        }


class ProductionResults(BaseModel):
    count: int = Field(default=0)
    results: List[Production] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "count": "1",
                "results": [{
                    "id": "299534",
                    "title": "Avengers: Endgame",
                    "overview": "After the devastating events of Avengers: Infinity War...",
                    "release_date": "2019-04-26",
                    "type": "movie",
                    "poster": "or06FN3Dka5tukK1e9sl16pB3iy.jpg",
                }]
            }
        }
