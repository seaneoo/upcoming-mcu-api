from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.errors import (exception_handler, http_exception_handler,
                        value_error_handler)
from app.limiter import limiter
from app.router import v1

app = FastAPI(title="Upcoming MCU API",
              description="""The timeline of the upcoming releases in the Marvel Cinematic Universe.
              This product uses the TMDB API but is not endorsed or certified by TMDB.""",
              version=1.0,
              contact={"email": "so@seano.dev"},
              license_info={"name": "Creative Commons Zero v1.0 Universal", "url": "https://github.com/seaneoo/upcoming-mcu-api/blob/main/LICENSE"})

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['*'])
app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(v1.router)


@app.get('/', include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')
