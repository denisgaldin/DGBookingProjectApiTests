import requests
import os
from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoint import Endpoints
from core.settings.config import Users, Timeouts
import allure

load_dotenv()


class APIClient:
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")

        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f"Unsupported environment value: {environment_str}")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            "Content-Type": "application/json",
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PROD:
            return os.getenv("PROD_BASE_URL")
        else:
            raise ValueError(f"Unsupported environment value: {environment}")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()
        with allure.step("Assert status code"):
            assert response.status_code == 201, f"Expected status 201 but got {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            payload = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()
        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        token = response.json().get("access_token")
        with allure.step("Updating header with authentication"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self, booking_id):
        with allure.step("Get booking by id"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{booking_id}"
            headers = {"Accept": "application/json"}
            response = self.session.get(url, headers=headers, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step("Assert status code"):
            assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
        with allure.step("Checking response"):
            booking_data = response.json()
            assert isinstance(booking_data, dict), f"Expected dict but got {type(booking_data)}"
        required_fields = ['firstname', 'last', 'totalprice', 'depositpaid', "bookingdates", "additionalneeds"]
        for field in required_fields:
            assert field in booking_data, f"Expected field {field} not in booking data"
        assert isinstance(booking_data["firstname"], str), "firstname should be string"
        assert isinstance(booking_data["lastname"], str), "lastname should be string"
        assert isinstance(booking_data["totalprice"], (int, float)), "totalprice should be number"
        assert isinstance(booking_data["depositpaid"], bool), "depositpaid should be boolean"
        assert isinstance(booking_data["bookingdates"], dict), "bookingdates should be object"
        assert isinstance(booking_data["additionalneeds"], str), "additionalneeds should be string"

        assert "checkin" in booking_data["bookingdates"], "Missing checkin date"
        assert "checkout" in booking_data["bookingdates"], "Missing checkout date"
        assert isinstance(booking_data["bookingdates"]["checkin"], str), "checkin should be string"
        assert isinstance(booking_data["bookingdates"]["checkout"], str), "checkout should be string"
