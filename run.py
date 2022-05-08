from app import app
from db import db


db.init_app(app)


@app.before_first_request
def creatr_table():
    db.create_all()
