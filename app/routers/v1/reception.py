from typing import Dict

from fastapi import APIRouter

router = APIRouter(tags=["reception"])


@router.get("/reception")
def read_root() -> Dict[str, str]:
    return {"Hello": "World"}
