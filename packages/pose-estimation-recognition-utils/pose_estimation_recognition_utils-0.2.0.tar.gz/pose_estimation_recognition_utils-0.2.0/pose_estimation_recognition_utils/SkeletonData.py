# Copyright 2025 Jonas David Stephan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SkeletonData.py

This module defines a class for managing skeleton data, including data points and frame information.

Author: Jonas David Stephan
Date: 2025-04-25
License: Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

import warnings

from .VideoSkeletonData import VideoSkeletonData


class SkeletonData(VideoSkeletonData):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Deprecated since 0.2.0 – will be removed in 0.3.0. Please use VideoSkeletonData",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(*args, **kwargs)