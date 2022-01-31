#    Copyright 2021 Invana
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http:www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
import pytest
from invana.connector.data_types import ShortType


class TestShortType:

    def test_short_type(self):
        a = ShortType(128)
        assert isinstance(a, int)
        assert a == 128

    def test_short_type_failure(self):
        with pytest.raises(ValueError) as exec_info:
            ShortType(12123123213123123211)
        assert exec_info.value.__str__() == 'ShortType value must be between -32768 and 32767 inclusive'
