import json
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar('T', bound='BaseModel')


class ExtDeserializableGeneric():

    @staticmethod
    def json_to_obj(json_object:str, obj_type:type[T])->T:
        try:
            serializable_data = obj_type(**json.loads(json_object))

            return serializable_data
        except Exception as ex:
            print(f"Error ExtDeserializableGeneric.json_to_obj converter: {ex}")