import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.errors import (exception_handler, http_exception_handler,
                        value_error_handler)
from app.limiter import RATE_LIMIT, limiter
from app.router import v1

app = FastAPI()

origins = [""]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(v1.router)


@app.get('/')
@limiter.limit(RATE_LIMIT)
async def root():
    quotes = ["I love you 3000.", "I am Iron Man.",
              "Avengers...assemble.", "I am Groot.", "Hail Hydra."]
    return JSONResponse(random.choice(quotes), media_type='text/plain')
