"""Pydanticモデル"""

from typing import Optional, TypedDict

from pydantic import BaseModel, ValidationInfo, field_validator, model_validator

from db import Item, Session


class ValidationContext(TypedDict):
    """model_validate()関数に渡すためのcontext"""

    db: Session
    items_cache: Optional[list[Item]]


class CreateRequest(BaseModel):
    """新しいアイテムを作成するリクエスト"""

    name: str

    @model_validator(mode="before")
    def is_under_limit(self, info: ValidationInfo):
        """アイテムの最大数を超えないかどうかの確認"""
        context: Optional[ValidationContext] = info.context
        # contextがない場合は確認できないのでスキップ
        if not context:
            return self
        # 最初のバリデータでDBから取得
        items = context["db"].get_all()
        if len(items) >= 5:
            raise ValueError("max 5 items.")
        # contextに格納して2つ目以降のバリデータで使えるようにする
        context["items_cache"] = items
        return self

    @field_validator("name")
    @classmethod
    def is_unique_name(cls, v: str, info: ValidationInfo):
        context: Optional[ValidationContext] = info.context
        # contextがない場合は確認できないのでスキップ
        if not context:
            return v
        # 2つめ以降のバリデータではDBから取得せずキャッシュを使用
        if context["items_cache"] is None:
            raise RuntimeError()
        matched = [i for i in context["items_cache"] if i.name == v]
        if matched:
            raise ValueError("name must be unique.")
        return v
