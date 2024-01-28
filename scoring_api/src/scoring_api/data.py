from typing import Any

from .constants import ADMIN_LOGIN
from .fields import (
    ArgumentsField, 
    BirthDayField,
    CharField,
    ClientIDsField, 
    DateField, 
    EmailField,
    Field, 
    GenderField, 
    PhoneField,
)


class DataMeta(type):

    def __init__(cls, clsname, bases, namespace) -> None:
        cls._fields = DataMeta._get_fields(namespace)
        super().__init__(clsname, bases, namespace)
    
    def __call__(cls, *args, **kwargs) -> Any:
        instance = super().__call__(*args, **kwargs)
        set_fields_names = []
        for name, value in kwargs.items():
            if name in cls._fields:
                setattr(instance, name, value)
                set_fields_names.append(name)
        not_set_fields = (field for name, field in cls._fields.items() if name not in set_fields_names)
        for field in not_set_fields:
            field.validate()
        if hasattr(cls, 'validate'):
            if not instance.validate():
                raise ValueError
        return instance

    @staticmethod
    def _get_fields(namespace: dict) -> dict:
        return {key: value for key, value in namespace.items() if isinstance(value, Field)}


class Data(metaclass=DataMeta):

    def __init__(self, **kwargs) -> None:
        ...


class MethodData(Data):
    
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self) -> bool:
        return self.login == ADMIN_LOGIN


class OnlineScoreData(Data):

    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    @property
    def has(self) -> list[str]:
        return [name for name, value in self._fields.items() if value.__get__(self, type(self)) is not None]

    def validate(self) -> None:
        if self.first_name and self.email:
            return True
        if self.first_name and self.last_name:
            return True
        if self.gender is not None and self.birthday:
            return True
        return False


class ClientsInterestsData(Data):

    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)

    @property
    def clients(self) -> int:
        return len(self.client_ids)
