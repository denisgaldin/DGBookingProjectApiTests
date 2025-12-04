import allure
import pytest
import requests


@allure.feature("Test ping")
@allure.story("Test connection")
def test_ping(api_client):
    status_code = api_client.ping()
    assert status_code == 201, f"Expected 201 status but got {status_code}"

