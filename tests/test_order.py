import allure
from data import TestMessages, URL, CourierService, color_selection
from helpers import Order
import pytest

# Класс с тестами для заказа
class TestCreateOrder:
    @allure.title('Проверка возможности создать заказ с использованием валидных данных и выбором цвета')
    @allure.description('Отправляем запрос POST api/v1/orders создания заказа с валидными данными и указанием значения тестируемого параметра, проверяем код и тело ответа')
    @allure.link(URL, name='«Яндекс.Самокат»')

    @pytest.mark.parametrize('color', color_selection)
    def test_create_order_successful_creation(self, random_order, color):
        random_order["color"] = color
        response = Order.create_order(random_order)
        assert response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION_WITH_VALID_VALUES["code"]
        assert TestMessages.ORDER_SUCCESSFUL_CREATION_WITH_VALID_VALUES["message"] in response.json()


# Kласс с тестами для проверки получения списка заказов
class TestListOfOrders:

    @allure.title('получение списка заказов')
    @allure.description('Получение списка заказов (код - 200 и "orders" в ответе)')
    @allure.link(URL, name='Учебный сервис «Яндекс.Самокат»')
    def test_get_list_of_orders_successful(self):
        response = Order.view_orders()
        assert response.status_code == TestMessages.ORDER_GET_LIST_OF_ORDERS["code"]
        assert TestMessages.ORDER_GET_LIST_OF_ORDERS["message"] in response.json()