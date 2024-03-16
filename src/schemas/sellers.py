from pydantic import BaseModel
from src.schemas.books import ReturnedBookNoSeller


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str


class ReturnedSeller(BaseSeller):
    id: int


class ReturnedSellerNoConfData(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str


# Класс для возврата массива объектов "Продавец", но без приватной информации (пароль)
class ReturnedAllSellersNoConfData(BaseModel):
    sellers: list[ReturnedSellerNoConfData]


# возврат продавца с его списком книг (без пароля)
class ReturnedSellersBooks(ReturnedSellerNoConfData):
    books: list[ReturnedBookNoSeller]
