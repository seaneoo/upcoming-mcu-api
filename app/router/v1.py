from fastapi import APIRouter, Request

router = APIRouter(
    prefix='/v1'
)


@router.get('/me')
async def me(request: Request):
    return {"host": request.client.host, "port": request.client.port}
