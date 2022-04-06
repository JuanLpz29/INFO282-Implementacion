from locust import HttpUser, task


class Test(HttpUser):
    @task
    def test_api(self):
        self.client.get("")
        self.client.get("")
