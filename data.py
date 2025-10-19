URL = 'https://qa-scooter.praktikum-services.ru/'

class Endpoints:

# Request_URL
    LOGIN_COURIER_URL = f"{URL}api/v1/courier/login"
    CREATE_COURIER_URL = f"{URL}api/v1/courier"
    DELETE_COURIER_URL = f"{URL}api/v1/courier/"

    CREATE_ORDER_URL = f"{URL}api/v1/orders"
    ORDERS_LIST_URL = f"{URL}api/v1/orders"
    ACCEPT_ORDER_URL = f"{URL}api/v1/orders/accept/"
    CANCEL_ORDER_URL = f"{URL}api/v1/orders/cancel/"
    VIEW_ORDER_URL = f"{URL}api/v1/orders/track"


# класс содержит КОДЫ и СООБЩЕНИЕ ответов на запросы
class TestMessages:

#создание курьера
    SUCCESSFUL_CREATED_NEW_COURIER_WITH_VALID_VALUES = {"code": 201, "message": True}
    COURIER_LOGIN_ALREADY_IN_USE = {"code": 409, "message": "Этот логин уже используется. Попробуйте другой."}
    COURIER_NOT_CREATED_WITHOUT_LOGIN_OR_PASSWORD = {"code": 400, "message": "Недостаточно данных для создания учетной записи"}

#логин курьера
    COURIER_SUCCESSFUL_AUTHORIZATION_WITH_VALID_VALUES = {"code": 200, "message": None}
    COURIER_NOT_ENOUGH_AUTHORIZATION_WITHOUT_LOGIN_OR_PASSWORD = {"code": 400, "message": "Недостаточно данных для входа"}
    COURIER_NOT_ENOUGH_AUTHORIZATION_WITH_WRONG_LOGIN_OR_PASSWORD = {"code": 404, "message": "Учетная запись не найдена"}

#удаление курьера
    COURIER_SUCCESSFUL_DELETING_WITH_EXISTING_ID = {"code": 200, "message": True}
    COURIER_DELETE_WITH_NOT_EXISTING_ID = {"code": 404, "message": "Курьера с таким id нет."}
    COURIER_DELETE_WITHOUT_ID = {"code": 400, "message": "Курьера с таким id нет."}

#создание заказа
    ORDER_SUCCESSFUL_CREATION_WITH_VALID_VALUES = {"code": 201, "message": "track"}

#список заказов
    ORDER_GET_LIST_OF_ORDERS = {"code": 200, "message": "orders"}

# переменная содержит выбор цвета самоката
color_selection = [ [],["BLACK"],["GREY"],["BLACK", "GREY"] ]

class CourierService:
    # переменная содержит параметры которые можно исключить при попытке авторизации
    EXCLUDE_PARAMETERS = {
        "login": "login",
        "password": "password",
        "firstName": "firstName"
    }
    # переменная содержит значения для изменения логина и пароля при попытке авторизации
    CHANGE_PARAMETERS = {
        "login": "wrong_login",
        "password": "wrong_password"
    }

