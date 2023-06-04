from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.errors import (exception_handler, http_exception_handler,
                        value_error_handler)
from app.router import v1

app = FastAPI()

origins = [""]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(Exception, exception_handler)

app.include_router(v1.router)
