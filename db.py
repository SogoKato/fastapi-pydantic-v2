"""ダミーのデータベース"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Item:
    """アイテム"""

    id: Optional[int] = field(init=False)
    name: str


data: list[Item] = []
last_id: int = -1


class Session:
    """DB操作のためのクラス"""

    def get_all(self) -> list[Item]:
        return data

    def add(self, d: Item) -> int:
        global last_id
        last_id += 1
        d.id = last_id
        data.append(d)
        return last_id
