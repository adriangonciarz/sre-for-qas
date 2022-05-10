import dataclasses
import random
import time
import uuid
from functools import wraps
from typing import Optional

from flask import request

from flask_restful import Resource


@dataclasses.dataclass
class Animal:
    name: str
    kind: str
    age: int
    id: str

    def to_json(self):
        return {
            'name': self.name,
            'kind': self.kind,
            'age': self.age,
            'id': self.id
        }


animals = [
    Animal('Azor', 'dog', 4, '55914dc6-5d2a-4963-afdc-dfa8787a8e28'),
    Animal('Fredzia', 'hamster', 1, '8de25da0-48ca-46a2-99bf-86c346729323')
]


def find_animal_with_id(animal_id) -> Optional[Animal]:
    return next((a for a in animals if a.id == animal_id), None)


def delete_animal_with_id(animal_id) -> Optional[Animal]:
    for idx, animal in enumerate(animals):
        if animal.id == animal_id:
            animal_to_delete_index = idx
            break
    animals.pop(animal_to_delete_index)


class HelloController(Resource):
    def get(self):
        return {'hello': 'world'}


class ReturnAlwaysOkController(Resource):
    def get(self):
        return {'status': 'ok'}, 200


class EchoStatusController(Resource):
    @staticmethod
    def post(status_code):
        if 100 <= status_code < 599:
            return {'status': status_code}, status_code
        else:
            return {'error': f'Unsupported status code {status_code}'}, 400


class AnimalsController(Resource):
    def post(self):
        name = request.json['name']
        kind = request.json['kind']
        age = request.json['age']
        id = str(uuid.uuid4())
        a = Animal(name, kind, age, id)
        animals.append(a)
        return a.to_json(), 200

    def get(self):
        return [a.to_json() for a in animals]


class AnimalDetailsController(Resource):
    @staticmethod
    def get(animal_id):
        animal = find_animal_with_id(animal_id)
        if animal:
            return animal.to_json()
        else:
            return '', 404

    @staticmethod
    def delete(animal_id):
        animal = find_animal_with_id(animal_id)
        if animal:
            delete_animal_with_id(animal_id)
            return '', 204
        else:
            return '', 404

    @staticmethod
    def put(animal_id):
        animal = find_animal_with_id(animal_id)
        if animal:
            name = request.json['name']
            kind = request.json['kind']
            age = request.json['age']
            animal.name = name
            animal.kind = kind
            animal.age = age
            return animal.to_json(), 202
        else:
            return '', 404


class ErrorController(Resource):
    def get(self):
        if random.randint(0, 1):
            return 'ok', 200
        else:
            time.sleep(random.random() * 0.2)
            return 'oopsie', 500
