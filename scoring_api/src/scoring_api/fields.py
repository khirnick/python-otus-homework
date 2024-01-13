from abc import ABC
import datetime
from typing import Any
from weakref import WeakKeyDictionary


class Field(ABC):

    def __init__(self, required: bool = True, nullable: bool = False) -> None:
        self.required = required
        self.nullable = nullable
        self.data = WeakKeyDictionary()
    
    def validate(self, instance: Any) -> None:
        if self.required and instance not in self.data:
            raise ValueError('Value must be provided')
        if not self.nullable and instance in self.data and self.data[instance] is None:
            raise ValueError('Value must not be nullable')

    def __get__(self, instance: Any, cls: Any) -> Any:
        return self.data.get(instance)

    def __set__(self, instance: Any, value: Any) -> None:
        self.data[instance] = value


class CharField(Field):
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f'{value} is not string')


class ArgumentsField(Field):
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if not isinstance(value, dict):
                raise ValueError(f'{value} is not a dict')


class EmailField(CharField):
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if '@' not in value:
                raise ValueError(f'{value} is not a valid email')


class PhoneField(Field):
    
    LENGTH = 11
    PHONE_REGION = '7'

    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if not isinstance(value, (str, int)):
                raise ValueError(f'{value} is not a string or int')
            value = str(value)
            if len(value) != self.LENGTH:
                raise ValueError(f'{value} length must be {self.LENGTH}')
            if not value.startswith(self.PHONE_REGION):
                raise ValueError(f'{value} must starts with {self.PHONE_REGION}')


class DateField(Field):
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            try:
                datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError(f'{value} is not valid date DD.MM.YYYY')


class BirthDayField(Field):

    MAX_AGE = 70

    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            try:
                parsed = datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError(f'{value} is not valid date DD.MM.YYYY')
            if datetime.datetime.utcnow().year - parsed.year > self.MAX_AGE:
                raise ValueError(f'{value} limits max age {self.MAX_AGE}')
            


class GenderField(Field):

    VALID = frozenset([0, 1, 2])
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if value not in self.VALID:
                raise ValueError(f'{value} is not in {self.VALID}')


class ClientIDsField(Field):
    
    def validate(self, instance: Any) -> None:
        super().validate(instance)
        value = self.data.get(instance)
        if value is not None:
            if not isinstance(value, list):
                raise ValueError(f'{value} is not a list')
            if any(item for item in value if not isinstance(item, int)):
                raise ValueError(f'{value} contains non integer values')
