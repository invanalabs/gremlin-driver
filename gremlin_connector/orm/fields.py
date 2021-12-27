#   Copyright 2021 Invana
#  #
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#  #
#    http:www.apache.org/licenses/LICENSE-2.0
#  #
#    Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
import datetime
import typing
from abc import ABC

from gremlin_python.statics import FloatType, LongType, SingleChar, SingleByte, ListType, SetType, ByteBufferType, \
    IntType
import abc

from gremlin_connector.orm.exceptions import ValidationError
from gremlin_connector.orm.models import ModelBase


class FieldBase:
    data_type = None

    def __init__(self, *,
                 default: typing.Any = None,
                 index: bool = False,
                 unique: bool = False,
                 allow_null: bool = False,
                 read_only: bool = False,
                 **kwargs):
        self.allow_null = allow_null
        self.index = index
        self.unique = unique
        self.default = default
        self.allow_null = allow_null
        self.read_only = read_only
        # self.validator = self.get_validator(*, **kwargs)

    def get_field_type(self):
        return self.data_type

    def validate(self, value, field_name=None, model=None):
        return NotImplementedError()

    def get_validator(self, **kwargs):
        raise NotImplementedError()  # pragma: no cover


class StringField(FieldBase, ABC):
    data_type = str

    def __init__(self, max_length=None, min_length=None, trim_whitespaces=True, **kwargs):
        if max_length is None and min_length is None:
            raise ValidationError(f"Either min_length or max_length should be provided for {self.__name__}")
        # assert max_length is not None, "max_length is required"
        super().__init__(**kwargs)
        self.max_length = max_length
        self.min_length = min_length
        self.trim_whitespaces = trim_whitespaces

    def validate(self, value, field_name=None, model=None):
        assert value is None or isinstance(value, str)
        assert self.max_length is None or isinstance(self.max_length, int)
        assert self.min_length is None or isinstance(self.min_length, int)
        assert self.allow_null is None or isinstance(self.allow_null, bool)
        assert self.trim_whitespaces is None or isinstance(self.trim_whitespaces, bool)
        if value is None and self.default:
            value = self.default

        if value is not None and self.trim_whitespaces is True:
            value = value.strip()

        if self.allow_null is False and value is None:
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be null when allow_null is False")

        if value:
            if self.max_length and value.__len__() > self.max_length:
                raise ValidationError(
                    f"max_length for field '{model.label_name}{field_name}' is {self.max_length} but the value has {value.__len__()}")
            if self.min_length and value.__len__() < self.min_length:
                raise ValidationError(
                    f"min_length for field '{model.label_name}{field_name}' is {self.min_length} but the value has {value.__len__()}")

        return self.data_type(value) if value else value


class BooleanField(FieldBase, ABC):
    data_type = bool

    def validate(self, value, field_name=None, model=None):
        if value and not isinstance(value, self.data_type):
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be '{value}'. must be a boolean")
        assert value is None or isinstance(value, self.data_type)
        if self.default:
            assert self.default is None or isinstance(self.default, bool)
        if value is None and self.default:
            value = self.default

        return self.data_type(value) if value is not None else value


class NumberFieldBase(FieldBase, ABC):

    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value, field_name=None, model=None):
        if value and not isinstance(value, self.data_type):
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be of type {type(value)},"
                                  f" expecting {self.data_type}")

        assert self.max_value is None or isinstance(self.max_value, int)
        assert self.min_value is None or isinstance(self.min_value, int)
        assert self.allow_null is None or isinstance(self.allow_null, bool)
        if value is None and self.default:
            value = self.default

        if self.allow_null is False and value is None:
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be null when allow_null is False")

        if value:
            if self.max_value and value > self.max_value:
                raise ValidationError(
                    f"max_value for field '{model.label_name}{field_name}' is {self.max_value} but the value has {value}")
            if self.min_value and value < self.min_value:
                raise ValidationError(
                    f"min_value for field '{model.label_name}{field_name}' is {self.min_value} but the value has {value}")

        return self.data_type(value) if value else value


class IntegerField(NumberFieldBase, ABC):
    data_type = IntType


class FloatField(NumberFieldBase, ABC):
    data_type = FloatType


# class DateFieldBase(FieldBase, ABC):


#
# class DateField(DateFieldBase, ABC):
#     data_type = datetime.datetime
#

class DateTimeField(FieldBase, ABC):
    data_type = datetime.datetime

    def validate(self, value, field_name=None, model=None):

        if value is None and self.default:
            value = self.default()
        if value and not isinstance(value, self.data_type):
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be of type {type(value)},"
                                  f" expecting {self.data_type}")
        if self.allow_null is False and value is None:
            raise ValidationError(f"field '{model.label_name}.{field_name}' cannot be null when allow_null is False")
        return value

#
# class LongField(NumberFieldBase, ABC):
#     data_type = LongType
#
#
# class DoubleField(FieldBase):
#     data_type = None
#
# class ByteField(FieldBase, ABC):
#     data_type = ByteBufferType
#
# class InstantField(FieldBase):
#     pass
#
# class GeoshapeField(FieldBase):
#     data_type = None
#
# class UUIDField(FieldBase):
#     pass
