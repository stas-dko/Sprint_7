import allure
from data import TestMessages, URL, CourierService
from helpers import Courier
import pytest

# Тесты для регистрации курьера
class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера с валидными данными')
    @allure.description('Отправляем запрос POST на ручку /api/v1/courier на создание курьера и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    def test_successful_created_new_courier_with_valid_values(self, random_courier):
        response = Courier.register_courier(random_courier)
        assert response.status_code == TestMessages.SUCCESSFUL_CREATED_NEW_COURIER_WITH_VALID_VALUES["code"]
        assert response.json()["ok"] == TestMessages.SUCCESSFUL_CREATED_NEW_COURIER_WITH_VALID_VALUES["message"]

    @allure.title('Проверка, что нельзя создать двух одинаковых курьеров')
    @allure.description('Отправляем запрос POST на ручку /api/v1/courier на невозможность создания курьера дважды и и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    def test_courier_login_already_in_use(self, random_courier):
        Courier.register_courier(random_courier)
        response = Courier.register_courier(random_courier)
        assert response.status_code == TestMessages.COURIER_LOGIN_ALREADY_IN_USE["code"]
        assert response.json()["message"] == TestMessages.COURIER_LOGIN_ALREADY_IN_USE["message"]

    @allure.title('Проверка регистрации курьера - json не содержит обязательного поля')
    @allure.description('Отправляем запрос POST на ручку /api/v1/courier на создание курьера и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    
    # параметризация для полей
    @pytest.mark.parametrize("field_to_exclude", [CourierService.EXCLUDE_PARAMETERS["login"], CourierService.EXCLUDE_PARAMETERS["password"]])

    def test_create_courier_without_required_field(self, random_courier, field_to_exclude):
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier, exclude=field_to_exclude)
        response = Courier.register_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_CREATED_WITHOUT_LOGIN_OR_PASSWORD["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_CREATED_WITHOUT_LOGIN_OR_PASSWORD["message"]

    @allure.title('Проверка регистрации курьера - json не содержит необязательного поля - "firstName"')
    @allure.description('Отправляем запрос POST на ручку /api/v1/courier на создание курьера и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    def test_create_courier_without_firstname_field_successful_created(self, random_courier):
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier,exclude=CourierService.EXCLUDE_PARAMETERS["firstName"])
        response = Courier.register_courier(payload)
        assert response.status_code == TestMessages.SUCCESSFUL_CREATED_NEW_COURIER_WITH_VALID_VALUES["code"]
        assert response.json()["ok"] == TestMessages.SUCCESSFUL_CREATED_NEW_COURIER_WITH_VALID_VALUES["message"]

# Тесты для авторизации курьера
class TestLoginCourier:

    @allure.title('Проверка авторизации существующего курьера с валидными данными')
    @allure.description(
        'Отправляем запрос POST на ручку /api/v1/courier/login на авторизацию курьера с указанием валидных значений и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    def test_login_courier_successful_authorized(self, random_courier):
        Courier.register_courier(random_courier)
        response = Courier.login_courier(random_courier)
        assert response.status_code == TestMessages.COURIER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES["code"]
        assert response.json()["id"] != TestMessages.COURIER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES["message"]

    @allure.title('Проверка авторизации существующего курьера - json не содержит обязательного поля- "login", "password"')
    @allure.description(
        'Отправляем запрос POST на ручку /api/v1/courier/login на авторизацию курьера без указания обязательного поля и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    @pytest.mark.parametrize("exclude_param", [CourierService.EXCLUDE_PARAMETERS["login"], CourierService.EXCLUDE_PARAMETERS["password"]])
    def test_login_courier_without_fields_not_authorized(self, random_courier, exclude_param):
        Courier.register_courier(random_courier)
        payload = Courier.excludes_parameter_from_courier_registration_data(random_courier, exclude=exclude_param)
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITHOUT_LOGIN_OR_PASSWORD["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITHOUT_LOGIN_OR_PASSWORD["message"]

    @allure.title('Проверка невозможности авторизации существующего курьера с указанием неверного обязательного поля')
    @allure.description(
        'Отправляем запрос POST на ручку /api/v1/courier/login на авторизацию курьера с указанием неверного обязательного поля и проверяем код и тело ответа')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    @pytest.mark.parametrize("change_param", [CourierService.EXCLUDE_PARAMETERS["login"], CourierService.EXCLUDE_PARAMETERS["password"]])
    def test_courier_with_wrong_credentials(self, random_courier, change_param):
        Courier.register_courier(random_courier)
        payload = Courier.change_parameter_value_in_courier_registration_data(random_courier, change_param)
        response = Courier.login_courier(payload)
        assert response.status_code == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITH_WRONG_LOGIN_OR_PASSWORD["code"]
        assert response.json()["message"] == TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITH_WRONG_LOGIN_OR_PASSWORD["message"]


