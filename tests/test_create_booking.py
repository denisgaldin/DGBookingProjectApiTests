import allure
import pytest
import requests

from conftest import api_client, generate_random_booking_data


@allure.feature('Test creating Booking')
@allure.story('Positive: Creating booking with custom data')
def test_creating_booking_with_custom_data(api_client):
    with allure.step("Подготовка данных для  создания брони"):
        booking_data = generate_random_booking_data

    with allure.step("Отправка запроса и валидация"):
        response = api_client.create_booking(booking_data, expected_status_code=200)
        response_json = response.json()

    with allure.step("Проверка статуса ответа"):
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    with allure.step("Проверка параметров брони в ответе"):
        assert 'bookingid' in response_json, "В ответе отсутствует bookingid"
        assert isinstance(response_json['bookingid'], int), "bookingid должен быть числом"
        assert response_json['booking']['firstname'] == booking_data['firstname'], "firstname не совпадает с ожидаемым"
        assert response_json['booking']['lastname'] == booking_data['lastname'], "lastname не совпадает с ожидаемым"
        assert response_json['booking']['totalprice'] == booking_data[
            'totalprice'], "totalprice не совпадает с ожидаемым"
        assert response_json['booking']['depositpaid'] == booking_data[
            'depositpaid'], "depositpaid не совпадает с ожидаемым"
        assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "checkin не совпадает с ожидаемым"
        assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "checkout не совпадает с ожидаемым"
        assert response_json['booking']['additionalneeds'] == booking_data[
            'additionalneeds'], "additionalneeds не совпадает с ожидаемым"


@allure.feature('Test creating Booking')
@allure.story('Positive: Creating booking with custom data')
def test_creating_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    response_json = response.json()

    assert response_json['booking']['firstname'] == booking_data['firstname'], "firstname не совпадает с ожидаемым"
    assert response_json['booking']['lastname'] == booking_data['lastname'], "lastname не совпадает с ожидаемым"
    assert response_json['booking']['totalprice'] == booking_data['totalprice'], "totalprice не совпадает с ожидаемым"
    assert response_json['booking']['depositpaid'] == booking_data[
        'depositpaid'], "depositpaid не совпадает с ожидаемым"
    assert response_json['booking']['bookingdates']['checkin'] == booking_data['bookingdates'][
        'checkin'], "checkin не совпадает с ожидаемым"
    assert response_json['booking']['bookingdates']['checkout'] == booking_data['bookingdates'][
        'checkout'], "checkout не совпадает с ожидаемым"
    assert response_json['booking']['additionalneeds'] == booking_data[
        'additionalneeds'], "additionalneeds не совпадает с ожидаемым"


@allure.feature("Test creating booking")
@allure.story("Negative: Creating booking with empty data")
def test_creating_booking_with_empty_booking_data(api_client):
    booking_data = {}
    with allure.step('Checking status code'):
        with pytest.raises(requests.exceptions.HTTPError) as exc_info:
            api_client.create_booking(booking_data)
            assert exc_info.value.response.status_code == 500, f"Expected status 500 but got {exc_info.value.response.status_code}"
