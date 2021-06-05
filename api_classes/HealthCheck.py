from flask_restful import Resource,Api,reqparse


class Health_Checker(Resource):
    def __init__(self):
        super().__init__()

    def get(self):
        return 200

