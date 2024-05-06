from fastapi import APIRouter
from starlette.responses import Response


def create_router() -> APIRouter:
    router = APIRouter()

    @router.get("/health", tags=['operational'], summary="healthcheck")
    def health():
        return Response(status_code=200)

    return router
