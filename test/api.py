from fastapi import APIRouter

from .schemas import Bulletin

router = APIRouter()


@router.post('/the-most-fair-voting')
def choose_framework(voice: Bulletin):
    # Whatever you choose.
    return {'The winner is': 'FastAPI'}
