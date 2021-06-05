from flask import Flask
from flask_restful import Api
import api_classes

app = Flask(__name__)
api = Api(app)
api.add_resource(api_classes.Health_Checker,"/")
api.add_resource(api_classes.Model_Server,"/image_classifier")