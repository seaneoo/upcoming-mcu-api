from http import HTTPStatus
from typing import List

from fastapi import APIRouter, HTTPException

from app.lib.database import collection
from app.limiter import RATE_LIMIT, limiter
from app.models.v1 import Production, ProductionResults
from app.utils import date as dateutils

router = APIRouter(
    prefix='/v1'
)


@router.get('/', response_model=Production)
@limiter.limit(RATE_LIMIT)
async def get_next_production(date: str = dateutils.format_datetime(dateutils.get_current_datetime())):
    productions: List[Production] = await collection.find().sort('release_date').to_list(1000)
    productions = [Production(**x) for x in productions]
    next_production = next((x for x in productions if x.release_date and dateutils.parse_date(
        x.release_date) > dateutils.parse_date(date)), None)

    if not next_production:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return next_production


@router.get('/all', response_model=ProductionResults)
@limiter.limit(RATE_LIMIT)
async def get_all_productions():
    productions = await collection.find().sort('release_date').to_list(1000)
    return {"count": len(productions), "results": productions}


@router.get('/{id}', response_model=ProductionResults)
@limiter.limit(RATE_LIMIT)
async def get_production(id: str):
    if (production := await collection.find({'tmdbId': id}).sort('release_date').to_list(1000)) is not None:
        return {"count": len(production), "results": production}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
