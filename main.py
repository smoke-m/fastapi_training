from fastapi import FastAPI
from typing import Optional
from enum import Enum

# Создание объекта приложения.
app = FastAPI(docs_url='/swagger')


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее специальное образование'
    HIGHER = 'Высшее образование'


@app.get('/me')
def hello_author():
    return {'Hello': 'author'}


@app.get('/{name}')
def greetings(
        name: str,
        surname: str,
        age: Optional[int] = None,
        is_staff: bool = False,
        education_level: Optional[EducationLevel] = None,
) -> dict[str, str]:
    result = ' '.join([name, surname])
    result = result.title()
    if age is not None:
        result += ', ' + str(age)
    if education_level is not None:
        result += ', ' + education_level.lower()
    if is_staff:
        result += ', сотрудник'
    return {'Hello': result}
