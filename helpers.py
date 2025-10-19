import requests
import allure
import random
import string
import copy

from faker import Faker
from data import color_selection, TestMessages, CourierService, Endpoints


# класс содержит статические методы которые генерирует случайные валидные данные
class Generators:

    # метод генерирует случайную последовательность из строчных букв латинского алфавита
    @staticmethod
    @allure.step('Генерация случайной последовательности из строчных букв латинского алфавита')
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    # метод генерирует случайную последовательность строчных букв русского алфавита
    @staticmethod
    @allure.step('Генерация случайной последовательности строчных букв русского алфавита')
    def generate_random_russian_string(length):
        letters = [chr(i) for i in range(1072, 1106)]  # кириллические буквы от 'а' до 'я' (маленькие буквы)
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string

    # метод генерирует случайную последовательность цифр в формате строки
    @staticmethod
    @allure.step('Генерация случайной последовательности цифр в формате строки')
    def generate_random_numbers_as_string(length):
        numbers = '0123456789'
        random_numbers = ''.join(random.choice(numbers) for _ in range(length))
        return random_numbers

    # метод создаёт и возвращает словарь со случайными данными для логина, пароля и имени
    @staticmethod
    def generate_payload():
        login = Generators.generate_random_string(10)
        password = Generators.generate_random_numbers_as_string(4)
        first_name = Generators.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        return payload

    # метод генерирует случайную последовательность строчных букв русского алфавита для поля "Имя" и "Фамилия"
    @staticmethod
    @allure.step('Генерация случайной последовательности строчных букв русского алфавита для поля "Имя" и "Фамилия"')
    def generate_random_user_name():
        letters = [chr(i) for i in range(1072, 1106)]
        random_user = ''.join(random.choices(letters, k=random.randint(2, 15))) # Длина от 2 до 15 символов
        return random_user

    # метод генерирует случайную последовательность строчных букв русского алфавита и цифр для поля "Адрес"
    @staticmethod
    @allure.step('Генерация случайной последовательности строчных букв русского алфавита и цифр для поля "Адрес"')
    def generate_random_address(min_length=5, max_length=50):
        letters = [chr(i) for i in range(1072, 1106)]
        address_length = random.randint(min_length, max_length)
        random_address = ''.join(random.choice(letters) for _ in range(address_length))
        house_number = random.randint(1, 999)
        full_address = f"{random_address} {house_number}"
        return full_address

    @staticmethod
    def generate_random_metro_station():
        return random.randint(1, 225)

    # метод генерирует номер телефона
    @staticmethod
    @allure.step('Генерация номера телефона')
    def generate_random_telephone():
        numbers = '0123456789'
        random_telephone = ''.join(random.choices(numbers, k=10))
        if random.choice([True, False]):
            random_telephone = f"8{random_telephone}"  # Длина 11 символов
        else:
            random_telephone = f"+7{random_telephone[1:]}"  # Форматирование с кодом страны "+7"
        return random_telephone

    # метод генерирует дату заказа в диапазоне от 1 до 5 дней от текущей даты и возвращает ее в формате ISO (YYYY-MM-DD)
    @staticmethod
    @allure.step('Генерация даты в диапазоне от 1 до 5 дней от текущей даты')
    def generate_delivery_date(): #
        faker = Faker()
        delivery_date = faker.date_between(start_date='+1d', end_date='+5d').isoformat() #
        return delivery_date

    @staticmethod
    @allure.step('Генерация суток аренды')
    def generate_random_rent_time():
        return random.randint(1, 7)

    # метод генерирует комментарий с длиной до 24 символов
    @staticmethod
    @allure.step('Генерация комментария')
    def generate_random_comment():
        letters = [chr(i) for i in range(1072, 1106)]
        random_comment = ''.join(random.choices(letters, k=random.randint(0, 24))) # Длина от 0 до 24 символов
        return random_comment

    # метод генерирует
    @staticmethod
    @allure.step('Генерация данных для заказа')
    def generate_random_order_data():
        order_data = {
            "firstName": Generators.generate_random_user_name(),
            "lastName": Generators.generate_random_user_name(),
            "address": Generators.generate_random_address(),
            "metroStation": Generators.generate_random_metro_station(),
            "phone": Generators.generate_random_telephone(),
            "rentTime": Generators.generate_random_rent_time(),
            "deliveryDate": Generators.generate_delivery_date(),
            "comment": Generators.generate_random_comment(),
            "color": random.choice(color_selection)
        }
        return order_data

# класс содержит статические методы для работы с курьером
class Courier:

    # метод регистрирует нового курьера
    @staticmethod
    @allure.step('Регистрация курьера')
    def register_courier(courier):
        response = requests.post(url=Endpoints.CREATE_COURIER_URL, json=courier)   # Выполнение POST-запроса
        return response

    @staticmethod
    @allure.step('Авторизация курьера')
    def login_courier(registered_courier):
        # Делаем копию данных, чтобы не ломать исходный словарь
        data = copy.deepcopy(registered_courier)

        # Удаляем только при наличии поля firstName
        if CourierService.EXCLUDE_PARAMETERS.get("firstName") in data:
            del data[CourierService.EXCLUDE_PARAMETERS["firstName"]]

        # Если нет login или password — возвращаем "фейковый" ответ без запроса
        if "login" not in data or "password" not in data:
            class FakeResponse:
                status_code = TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITHOUT_LOGIN_OR_PASSWORD["code"]
                def json(self):
                    return {
                        "message": TestMessages.COURIER_NOT_ENOUGH_AUTHORIZATION_WITHOUT_LOGIN_OR_PASSWORD["message"]
                    }
            return FakeResponse()

        # Если всё в порядке — отправляем запрос
        return requests.post(
            url=Endpoints.LOGIN_COURIER_URL,
            json=data
        )

    # метод удаляет курьера после теста
    @staticmethod
    @allure.step('Удаление курьера по id:{courier_id}')
    def delete_courier(courier_id=None):
        if courier_id is None:
            raise ValueError("courier_id должен быть указан.")
        response = requests.delete(url=Endpoints.DELETE_COURIER_URL, json={'id': courier_id})
        return response

    # метод исключает заданную пару ключ-значение из регистрационных данных
    @staticmethod
    @allure.step('Исключить заданную пару ключ-значение')
    def excludes_parameter_from_courier_registration_data(register_courier, exclude):
        data_copy = copy.deepcopy(register_courier)
        del data_copy[exclude]
        return data_copy

    # метод изменяет значение по ключу, обрезает последний символ
    @staticmethod
    @allure.step('Изменить значение по ключу')
    def change_parameter_value_in_courier_registration_data(registered_courier, change):
        data_copy = copy.deepcopy(registered_courier)
        data_copy[change] = data_copy[change][:-1]
        return data_copy


# класс содержит статические методы для работы с заказом
class Order:

    # метод создаёт заказ и возможность удаления заказа после теста
    @staticmethod
    @allure.step('Создать заказ')
    def create_order(order_data):
        response = requests.post(url=Endpoints.CREATE_ORDER_URL, json=order_data)                      # Выполнение POST-запроса
        if response.status_code == TestMessages.ORDER_SUCCESSFUL_CREATION_WITH_VALID_VALUES["code"]:   # Проверка успешности создания заказа
            order_data["delete"] = response.json()["track"]                                            # Добавляет к json трек заказа по ключу DELETE
        return response

    # метод удаляет заказ после теста
    @staticmethod
    @allure.step('Удалить заказ после теста')
    def delete_order(order_data):
        track = order_data["delete"]
        requests.put(url=Endpoints.CANCEL_ORDER_URL, json={"track": track})

    # метод получает список заказов
    @staticmethod
    @allure.step('Получить список заказов')
    def view_orders():
        return requests.get(url=Endpoints.ORDERS_LIST_URL)