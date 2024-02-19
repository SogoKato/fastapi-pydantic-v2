"""FastAPIのdependency"""

from typing import Type

from fastapi import Depends
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ValidationError

from db import Session
from model import ValidationContext


def get_db() -> Session:
    """DBセッションを取得する"""
    return Session()


def validate(model: Type[BaseModel]):
    """ユーザーの入力値を検証する関数を返す高階関数"""

    async def func(content: model, db: Session = Depends(get_db)) -> model:
        context = dict(ValidationContext(db=db, items_cache=None))
        try:
            model.model_validate(content.model_dump(), context=context)
        except ValidationError as e:
            raise RequestValidationError(errors=e.errors())
        return content

    return func
