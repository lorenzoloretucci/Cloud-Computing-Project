from flask_restful import Resource,Api,reqparse
from Classification_Model import Inception_Model
import boto3
import socket
model = Inception_Model()



class Model_Server(Resource):
    def __init__(self):
        super().__init__()
        self.image_parser = reqparse.RequestParser()
        self.image_parser.add_argument("image_name",type=str,help="Name of the image on the S3 service is required",required=True)


    def get(self):
        args = self.image_parser.parse_args()
        image_name = args["image_name"]

        s3 = boto3.resource('s3')
        s3.Bucket('userimages').download_file("preprocesseimages/"+image_name, '/home/ec2-user/image_to_model.jpg')
        predicted_class = model.return_prediction('/home/ec2-user/image_to_model.jpg')
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        data = {"url": predicted_class,"local_ip_adress":ip_address}
        return data, 200

