from abc import ABC
import datetime
from typing import Any
from weakref import WeakKeyDictionary

_NotSet = object()


class Field:

    def __init__(self, required: bool = True, nullable: bool = False) -> None:
        self.required = required
        self.nullable = nullable
        self.data = WeakKeyDictionary()

    def validate(self, value: Any = _NotSet) -> None:
        if self.required and value is _NotSet:
            raise ValueError('Value must be provided')
        if not self.nullable and value is None:
            raise ValueError('Value must not be nullable')

    def __get__(self, instance: Any, cls: Any) -> Any:
        return self.data.get(instance)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        self.data[instance] = value


class CharField(Field):
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if not isinstance(value, str):
                raise ValueError(f'{value} is not string')


class ArgumentsField(Field):
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if not isinstance(value, dict):
                raise ValueError(f'{value} is not a dict')


class EmailField(CharField):
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if '@' not in value:
                raise ValueError(f'{value} is not a valid email')


class PhoneField(Field):
    
    LENGTH = 11
    PHONE_REGION = '7'

    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if not isinstance(value, (str, int)):
                raise ValueError(f'{value} is not a string or int')
            value = str(value)
            if len(value) != self.LENGTH:
                raise ValueError(f'{value} length must be {self.LENGTH}')
            if not value.startswith(self.PHONE_REGION):
                raise ValueError(f'{value} must starts with {self.PHONE_REGION}')


class DateField(Field):
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            try:
                datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError(f'{value} is not valid date DD.MM.YYYY')


class BirthDayField(Field):

    MAX_AGE = 70

    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            try:
                parsed = datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError(f'{value} is not valid date DD.MM.YYYY')
            if datetime.datetime.utcnow().year - parsed.year > self.MAX_AGE:
                raise ValueError(f'{value} limits max age {self.MAX_AGE}')
            


class GenderField(Field):

    VALID = frozenset([0, 1, 2])
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if value not in self.VALID:
                raise ValueError(f'{value} is not in {self.VALID}')


class ClientIDsField(Field):
    
    def validate(self, value: Any = _NotSet) -> None:
        super().validate(value)
        if value is not None and value is not _NotSet:
            if not isinstance(value, list):
                raise ValueError(f'{value} is not a list')
            if any(item for item in value if not isinstance(item, int)):
                raise ValueError(f'{value} contains non integer values')
