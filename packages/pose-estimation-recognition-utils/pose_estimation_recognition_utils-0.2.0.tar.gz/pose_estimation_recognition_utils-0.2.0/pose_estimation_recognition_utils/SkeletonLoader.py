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
SkeletonLoader.py

This module provides functions to load and filter skeleton data from a JSON file, string, or object for video data

Author: Jonas David Stephan
Date: 2025-04-25
License: Apache License 2.0 (http://www.apache.org/licenses/LICENSE-2.0)
"""

import numpy as np
from typing import List
import warnings

from .VideoSkeletonLoader import load_video_skeleton, load_video_skeleton_object

def load_skeleton(file_path: str, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from a JSON file and filters the points based on specified ranges and individual points for video data.

    Args:
        file_path (str): Path to the JSON file containing the skeleton data.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    warnings.warn(
        "Deprecated since 0.2.0 – will be removed in 0.3.0. Please use load_video_skeleton",
        DeprecationWarning,
        stacklevel=2
    )
    return load_video_skeleton(file_path, points_to_include)

def load_skeleton_object(skeleton_object: List, points_to_include: str) -> np.ndarray:
    """
    Loads skeleton data from an object and filters the points based on specified ranges and individual points for video data.

    Args:
        skeleton_object (list): A list of frames, where each frame contains data points representing skeleton points.
        points_to_include (str): A string specifying the ranges and individual point IDs to include.
                                 Ranges and individual points are separated by commas.
                                 For example: "1-22,100-150,200".

    Returns:
        np.ndarray: A numpy array containing the filtered skeleton data.
    """
    warnings.warn(
        "Deprecated since 0.2.0 – will be removed in 0.3.0. Please use load_video_skeleton_object",
        DeprecationWarning,
        stacklevel=2
    )
    return load_video_skeleton_object(skeleton_object, points_to_include)