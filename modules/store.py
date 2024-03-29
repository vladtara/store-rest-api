from db import db
from modules.items import ItemJSON
from typing import Dict, List, Union

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]


class StoreModule(db.Model):
    __tablename__ = "stores"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    items = db.relationship('ItemModule', lazy='dynamic')

    def __init__(self, name: str):
        self.name = name

    def json(self) -> StoreJSON:
        return {
            'id': self.id,
            'name': self.name,
            'items': [i.json() for i in self.items.all()]}

    @ classmethod
    def find_by_name(cls, name: str) -> "StoreModule":
        return cls.query.filter_by(name=name).first()

    @ classmethod
    def select_all(cls) -> List["StoreModule"]:
        return cls.query.all()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
