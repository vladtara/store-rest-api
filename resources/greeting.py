from flask_restful import Resource
from typing import Dict


class Greeting(Resource):
    def get(self) -> Dict:
        return {"massage": "This is Store rest api"}
