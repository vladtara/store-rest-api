import flask_restful


from flask_restful import Resource


class Greeting(Resource):
    def get(self):
        return {"massage": "This is Store rest api"}
