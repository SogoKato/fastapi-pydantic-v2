from dataclasses import asdict
from typing import Annotated

from fastapi import Depends, FastAPI

from db import Item, Session
from dependency import get_db, validate
from model import CreateRequest

app = FastAPI()


@app.get("/items")
async def read_items(db: Annotated[Session, Depends(get_db)]):
    items = db.get_all()
    return {"items": items}


@app.post("/items")
async def create_item(
    db: Annotated[Session, Depends(get_db)],
    body: Annotated[CreateRequest, Depends(validate(CreateRequest))],
):
    item = Item(name=body.name)
    db.add(item)
    return {"item": asdict(item)}
