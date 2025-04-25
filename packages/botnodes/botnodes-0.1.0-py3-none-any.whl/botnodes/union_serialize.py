from abc import ABC, abstractmethod
from typing import Generic, Protocol, Self, TypeVar


JsonLikeDictItem = None | str | int | bool | list['JsonLikeDictItem'] | dict[str, 'JsonLikeDictItem']

JsonLikeDict = dict[str, JsonLikeDictItem]

class Model(Protocol):
    @classmethod
    @abstractmethod
    def model_validate(cls, obj: JsonLikeDict) -> Self:
        ...
    
    def model_dump(self) -> JsonLikeDict:
        ...

TModel = TypeVar('TModel', bound='Model')
        
class Serializer(ABC, Generic[TModel]):
    @abstractmethod
    def serialize(self, obj: TModel) -> JsonLikeDict:
        ...
        
    @abstractmethod
    def deserialize(self, dict: JsonLikeDict) -> TModel:
        ...
        
    @abstractmethod
    def get_served_models(self) -> set[type[TModel]]:
        ...
        
class End(Serializer[TModel], Generic[TModel]):
    def __init__(self, model: type[TModel]):
        self._model = model

    def serialize(self, obj: TModel) -> JsonLikeDict:
        return obj.model_dump()

    def deserialize(self, dict: JsonLikeDict) -> TModel:
        return self._model.model_validate(dict)

    def get_served_models(self):
        return {self._model}

class UnionSerializer(Serializer[TModel], Generic[TModel]):
    def __init__(self, discriminator: str, schema: dict[str, Serializer]):
        self._discriminator = discriminator

        self._key_to_serializer = schema
        self._serializer_to_key = {value: key for key, value in schema.items()}

        self._served_to_serializer: dict[type[TModel], Serializer[TModel]] = {}
        self._served = set()

        for serializer in schema.values():
            self._served.add(*serializer.get_served_models())
            for served in serializer.get_served_models():
                self._served_to_serializer[served] = serializer

    def serialize(self, obj: TModel) -> JsonLikeDict:
        serializer = self._served_to_serializer[type(obj)]

        key = self._serializer_to_key[serializer]

        serialized = serializer.serialize(obj)

        serialized[self._discriminator] = key

        return serialized

    def deserialize(self, dict: JsonLikeDict) -> TModel:
        key = dict.pop(self._discriminator)

        if not isinstance(key, str):
            raise ValueError('Invalid dict')

        return self._key_to_serializer[key].deserialize(dict)

    def get_served_models(self) -> set[type[TModel]]:
        return self._served
