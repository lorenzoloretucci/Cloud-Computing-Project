from locust import HttpUser, task, between


class WebsiteTestUser(HttpUser):
    #wait_time  that make our client wait between each task
    wait_time = between(0.1, 0.5)
    def image_payload(self, file_name, file_content_type='image/jpeg'):
        file_name = "/home/vedat/Desktop/"+file_name
        file_content = open(file_name, 'rb')

        return {"image_file":(file_name, file_content, file_content_type)}

    def yes_no_payload(self,answer = "yes"):
        payload = {"yes_or_no_group":answer}
        return payload


    @task(1)
    def get_classification_result(self):
        self.client.get("/")
        self.client.post("/up", files=self.image_payload("ee.jpg"))
        self.client.post("/feed_back",data=self.yes_no_payload())

    @task(1)
    def get_classification_result(self):
        self.client.get("/")
        self.client.post("/up", files=self.image_payload("ee.jpg"))
        self.client.post("/feed_back", data=self.yes_no_payload(answer="no"))
        self.client