import dataclasses as dc
from typing import Any

from bson import ObjectId


@dc.dataclass()
class Book:
    title: str
    author: str = dc.field(default=None)
    num_pages: int = dc.field(default=None)
    amount: int = dc.field(default=0)
    _id: ObjectId = dc.field(default=None)

    def to_insert (self) -> dict[str, Any]:
        if self._id is None:
            self._id = ObjectId()

        return {
            field.name: getattr(self, field.name)
            for field in dc.fields(self)
            if field.init and getattr(self, field.name) is not None
        }