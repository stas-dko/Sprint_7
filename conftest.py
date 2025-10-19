import pytest
from helpers import Generators, Courier, Order
import copy

# фикстура генерирует случайные данные курьера и удаляет после теста
@pytest.fixture()
def random_courier():
    random_courier = Generators.generate_payload()
    random_courier_copy = copy.deepcopy(random_courier) # создается копия сгенерированных данных
    yield random_courier
    Courier.delete_courier(random_courier_copy)  # удаляет курьера после теста

# фикстура генерирует случайные данные заказа и удаляет после теста
@pytest.fixture()
def random_order():
    random_order = Generators.generate_random_order_data()
    yield random_order
    Order.delete_order(random_order)  # удаляет заказ после теста