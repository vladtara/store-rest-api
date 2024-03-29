from db import db
from typing import Dict, Union

UserJSON = Dict[str, Union[str, int]]


class UserModule(db.Model):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def json(self) -> UserJSON:
        return {
            'id': self.id,
            'name': self.username
        }

    @classmethod
    def select_all(cls) -> "UserModule":
        return cls.query.all()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModule":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModule":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
