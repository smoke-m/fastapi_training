from typing import Optional

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(docs_url='/swagger')


class Cat(str, Enum):
    PRINTERS = 'Принтеры'
    MONITORS = 'Мониторы'
    DOP_OPS = 'Доп. оборудование'
    INPUT = 'Устройства ввода'


class Person(BaseModel):
    name: str
    surname: str
    age: Optional[int]
    is_staff: bool = False


class AuctionLot(BaseModel):
    category: Cat
    name_lot: str
    name_model: Optional[str]
    start_price: int = 1000
    seller: Person


@app.post('/new-lot')
def register_lot(lot: AuctionLot):
    # Здесь мог бы быть код для сохранения заявки,
    # но мы не станем его писать. И вам не надо.
    return {'result': 'Ваша заявка зарегистрирована!'}
