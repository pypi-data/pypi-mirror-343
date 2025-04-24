class RetryError(Exception):
    """
    Ошибка, которая вызывает повторный вызов запроса
    """


class MaxRetryError(Exception):
    """
    Превышено максимальное число повторов
    """


class InteractionError(Exception):
    """ Ошибки взаимодействия с внешним сервисом """

    def __init__(self, status_code, message):
        super().__init__(message)
        self.status_code = status_code
