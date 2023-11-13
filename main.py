from fastapi import FastAPI, Path, Query
from typing import Optional, Union
from enum import Enum, IntEnum
from pydantic import BaseModel

# Создание объекта приложения.
app = FastAPI(docs_url='/swagger')


class Tag(IntEnum):
    IMMUTABLE = 1
    MUTABLE = 2
    COMMON_METHODS = 3


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


@app.get('/me', tags=['special methods'], summary='Приветствие автора')
def hello_author() -> dict[str, str]:
    return {'Hello': 'author'}


@app.get('/{name}',
         #  tags=['common methods'],
         tags=[Tag(3).name.lower()],
         summary='Общее приветствие',
         response_description='Полная строка приветствия')
def greetings(
        *,
        # У параметров запроса name и surname значений по умолчанию нет,
        # поэтому в первый параметр ставим многоточие, Ellipsis.
        name: str = Path(
            ..., min_length=2, max_length=20,
            title='Полное имя', description='Можно вводить в любом регистре'
        ),
        surname: list[str] = Query(..., min_length=2, max_length=50),
        # gt означает "больше чем", le — "меньше чем или равно".
        age: Optional[int] = Query(None, ge=4, le=99),
        # Добавляем псевдоним 'is-staff'
        is_staff: bool = Query(
            False, alias='is-staff', include_in_schema=False
        ),
        education_level: Optional[EducationLevel] = None,
        cyrillic_string: str = Query('кириллица', regex='^[А-Яа-яЁё ]+$')
) -> dict[str, str]:
    """
    Приветствие пользователя:

    - **name**: имя
    - **surname**: фамилия
    - **age**: возраст (опционально)
    - **is_staff**: является ли пользователь сотрудником
    - **education_level**: уровень образования (опционально)
    """
    surnames = ' '.join(surname)
    result = ' '.join([name, surnames])
    result = result.title()
    if age is not None:
        result += ', ' + str(age)
    if education_level is not None:
        result += ', ' + education_level.lower()
    if is_staff:
        result += ', сотрудник'
    return {'Hello': result}


# Создадим класс Person, унаследованный от BaseModel;
# в атрибутах класса перечислим ожидаемые параметры запроса.
# Аннотируем атрибуты класса.
class Person(BaseModel):
    name: str
    surname: Union[str, list[str]]
    age: Optional[int]
    is_staff: bool = False
    education_level: Optional[EducationLevel]


# Меняем метод GET на POST, указываем статичный адрес.
@app.post('/hello')
# Вместо множества параметра теперь будет только один - person,
# в качестве аннотации указываем класс Person.
def greeting(person: Person) -> dict[str, str]:
    # Обращение к атрибутам класса происходит через точку;
    # при этом будут работать проверки на уровне типов данных.
    # В IDE будут работать автодополнения.
    if isinstance(person.surname, list):
        surnames = ' '.join(person.surname)
    else:
        surnames = person.surname
    result = ' '.join([person.name, surnames])
    result = result.title()
    if person.age is not None:
        result += ', ' + str(person.age)
    if person.education_level is not None:
        result += ', ' + person.education_level.lower()
    if person.is_staff:
        result += ', сотрудник'
    return {'Hello': result}
