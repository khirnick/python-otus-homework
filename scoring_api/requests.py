from constants import ADMIN_LOGIN
from fields import (
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


class RequestMeta(type):

    def __init__(cls, clsname, bases, namespace):
        cls._fields = RequestMeta._get_fields(namespace)
        super().__init__(clsname, bases, namespace)
    
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        for name, value in kwargs.items():
            if name in cls._fields:
                setattr(instance, name, value)
        for field in cls._fields.values():
            field.validate(instance)
        if hasattr(cls, 'validate'):
            instance.validate()
        return instance
    
    @staticmethod
    def _get_fields(namespace):
        return {key: value for key, value in namespace.items() if isinstance(value, Field)}


class Request(metaclass=RequestMeta):

    def __init__(self, **kwargs) -> None:
        ...


class OnlineScoreRequest(Request):

    first_name = CharField(required=False, nullable=True)
    last_name = CharField(required=False, nullable=True)
    email = EmailField(required=False, nullable=True)
    phone = PhoneField(required=False, nullable=True)
    birthday = BirthDayField(required=False, nullable=True)
    gender = GenderField(required=False, nullable=True)

    def validate(self):
        if self.first_name and self.email:
            return True
        if self.first_name and self.last_name:
            return True
        if self.gender is not None and self.birthday:
            return True
        return False


class ClientsInterestsRequest(Request):

    client_ids = ClientIDsField(required=True)
    date = DateField(required=False, nullable=True)


class MethodRequest(Request):
    
    account = CharField(required=False, nullable=True)
    login = CharField(required=True, nullable=True)
    token = CharField(required=True, nullable=True)
    arguments = ArgumentsField(required=True, nullable=True)
    method = CharField(required=True, nullable=False)

    @property
    def is_admin(self):
        return self.login == ADMIN_LOGIN
