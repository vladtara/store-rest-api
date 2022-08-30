from db import db


class Blocklist(db.Model):
    __tablename__ = "blocklist"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False)

    @classmethod
    def find_by_jti(cls, jti_id: int):
        return cls.query.filter_by(jti=jti_id).scalar()

    def add_jti(self) -> None:
        db.session.add(self)
        db.session.commit()
