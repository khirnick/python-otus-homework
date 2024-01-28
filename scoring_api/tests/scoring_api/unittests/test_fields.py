import datetime
from unittest import mock
import pytest
from scoring_api.fields import ArgumentsField, BirthDayField, CharField, ClientIDsField, DateField, EmailField, Field, GenderField, PhoneField


def test_CharField():
    class SomeClass:
        field = CharField()
    
    some_class = SomeClass()
    some_class.field = '123'
    with pytest.raises(ValueError):
        some_class.field = 123
    assert issubclass(CharField, Field)


def test_ArgumentsField():
    class SomeClass:
        field = ArgumentsField()
    
    some_class = SomeClass()
    some_class.field = {'a': 1, 'b': 2}
    with pytest.raises(ValueError):
        some_class.field = 123
    assert issubclass(ArgumentsField, Field)


def test_EmailField():
    class SomeClass:
        field = EmailField()
    
    some_class = SomeClass()
    some_class.field = 'some@email.example'
    with pytest.raises(ValueError):
        some_class.field = 123
    assert issubclass(EmailField, Field)


def test_PhoneField():
    class SomeClass:
        field = PhoneField()
    
    some_class = SomeClass()
    some_class.field = '71112223344'
    some_class.field = 71112223344
    with pytest.raises(ValueError):
        some_class.field = '711111111111111111'
    with pytest.raises(ValueError):
        some_class.field = '81112223344'
    assert issubclass(PhoneField, Field)


def test_DateField():
    class SomeClass:
        field = DateField()
    
    some_class = SomeClass()
    some_class.field = '01.01.1970'
    with pytest.raises(ValueError):
        some_class.field = '01011970'
    assert issubclass(DateField, Field)


def test_BirthdayField():
    class SomeClass:
        field = BirthDayField()
    
    some_class = SomeClass()
    some_class.field = '01.01.2000'
    with pytest.raises(ValueError):
        some_class.field = '01012000'
    with pytest.raises(ValueError):
        some_class.field = '01.01.1900'
    assert issubclass(BirthDayField, Field)



def test_GenderField():
    class SomeClass:
        field = GenderField()
    
    some_class = SomeClass()
    some_class.field = 0
    some_class.field = 1
    some_class.field = 2
    with pytest.raises(ValueError):
        some_class.field = 3
    assert issubclass(GenderField, Field)


def test_ClientIDsField():
    class SomeClass:
        field = ClientIDsField()
    
    some_class = SomeClass()
    some_class.field = [1, 2, 3]
    with pytest.raises(ValueError):
        some_class.field = [1, 2, '3']
    with pytest.raises(ValueError):
        some_class.field = 1
    assert issubclass(ClientIDsField, Field)
