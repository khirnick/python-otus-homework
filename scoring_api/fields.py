from abc import ABC
import datetime
from typing import Any
from weakref import WeakKeyDictionary


class Field(ABC):

    def __init__(self, required: bool = True, nullable: bool = False) -> None:
        self.required = required
        self.nullable = nullable
        self.data = WeakKeyDictionary()
    
    def validate(self, instance):
        if self.required and instance not in self.data:
            raise ValueError('Value is required')
        if not self.nullable and instance in self.data and self.data[instance] is None:
            raise ValueError('Value is null')

    def __get__(self, instance, cls):
        return self.data.get(instance)

    def __set__(self, instance, value):
        self.data[instance] = value


class CharField(Field):
    
    def __init__(self, required: bool = True, nullable: bool = False , min_len: int | None = None, max_len: int | None = None) -> None:
        super().__init__(required, nullable)
        if min_len is not None and min_len < 0:
            raise ValueError('min_len must be positive')
        if max_len is not None and max_len < 0:
            raise ValueError('max_len must be positive')
        if min_len and max_len and max_len < min_len:
            raise ValueError('max_len must be > min_len')
        self.min_len = min_len
        self.max_len = max_len
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if not isinstance(value, str):
                raise ValueError('Value must be string')
            if self.min_len and len(value) < self.min_len:
                raise ValueError(f'Value length must be > {self.min_len}')
            if self.max_len and len(value) > self.max_len:
                raise ValueError(f'Value length must be < {self.max_len}')


class ArgumentsField(Field):
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if not isinstance(value, dict):
                raise ValueError('Not a dict')


class EmailField(CharField):
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if '@' not in value:
                raise ValueError('Not a email')


class PhoneField(Field):
    
    LENGTH = 11
    PHONE_REGION = '7'

    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if not isinstance(value, (str, int)):
                raise ValueError('Value must be string or int')
            value = str(value)
            if len(value) != self.LENGTH:
                raise ValueError(f'Value length must be {self.LENGTH}')
            if not value.startswith(self.PHONE_REGION):
                raise ValueError(f'Value must starts with {self.PHONE_REGION}')


class DateField(Field):
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            try:
                datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Cannot parse datetime')


class BirthDayField(Field):

    MAX_AGE = 70

    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            try:
                parsed = datetime.datetime.strptime(value, '%d.%m.%Y')
            except ValueError:
                raise ValueError('Cannot parse datetime')
            if datetime.datetime.utcnow().year - parsed.year > self.MAX_AGE:
                raise ValueError(f'Limits max age: {self.MAX_AGE}')
            


class GenderField(Field):

    VALID = (0, 1, 2)
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if value not in self.VALID:
                raise ValueError(f'Not in valid: {self.VALID}')


class ClientIDsField(Field):
    
    def validate(self, instance):
        super().validate(instance)
        if instance in self.data:
            value = self.data[instance]
            if not isinstance(value, list):
                raise ValueError('Not a list')
            if any(item for item in value if not isinstance(item, int)):
                raise ValueError('Contains non-int values')
