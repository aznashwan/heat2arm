# Copyright 2015 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
    This module contains definitions for all functions and classes which are
    shared between CFN and Heat templates.
"""

from heat2arm.parser.common.base64_function import Base64Function
from heat2arm.parser.common.map_find import MapFindFunction
from heat2arm.parser.common.get_attr_function import GetAttrFunction
from heat2arm.parser.common.join_function import JoinFunction
from heat2arm.parser.common.ref_function import RefFunction
