from fastapi import FastAPI
from pydantic import BaseModel, root_validator

app = FastAPI()

FORBIDDEN_NAMES = [
    'Luke Skywalker',
    'Darth Vader',
    'Leia Organa',
    'Han Solo',
]


class Person(BaseModel):
    name: str
    surname: str

    @root_validator(skip_on_failure=True)
    def forbidden(cls, values):
        checked_value = ' '.join([values['name'].title(), values['surname'].title()])
        if checked_value in FORBIDDEN_NAMES:
            raise ValueError('Звёздные войны')
        return values


@app.post('/hello')
def greetings(person: Person) -> dict[str, str]:
    result = ' '.join([person.name, person.surname])
    result = result.title()
    return {'Hello': result}
