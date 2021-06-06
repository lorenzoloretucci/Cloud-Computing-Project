from flask_restful import Resource,Api,reqparse
from Classification_Model import Inception_Model
import boto3
import socket
model = Inception_Model()



class Model_Server(Resource):
    def __init__(self):
        global model
        super().__init__()
        self.image_parser = reqparse.RequestParser()
        self.image_parser.add_argument("image_name",type=str,help="Name of the image on the S3 service is required",required=True)
        self.s3= boto3.resource('s3')
        print(model.model_update_time)
        if not self.retrieve_model_weights_mdate(model.model_update_time):
            print("here")
            model= Inception_Model()


    def get(self):
        args = self.image_parser.parse_args()
        image_name = args["image_name"]
        self.s3.Bucket('userimages').download_file("preprocesseimages/"+image_name, '/home/ec2-user/image_to_model.jpg')
        predicted_class = model.return_prediction('/home/ec2-user/image_to_model.jpg')
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        data = {"url": predicted_class,"local_ip_adress":ip_address}
        return data, 200


    def retrieve_model_weights_mdate(self,model_date):
        obj = self.s3.Object("clc-project-mlmodels", "best_model_2_inc.h5")
        last_weight_version = obj.last_modified
        if last_weight_version == model_date:
            return True
        else:
            return False



