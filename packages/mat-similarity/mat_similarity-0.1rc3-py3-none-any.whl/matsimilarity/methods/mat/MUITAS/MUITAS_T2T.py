# -*- coding: utf-8 -*-
'''
MAT-Tools: Python Framework for Multiple Aspect Trajectory Data Mining

The present package offers a tool, to support the user in the task of data analysis of multiple aspect trajectories. It integrates into a unique framework for multiple aspects trajectories and in general for multidimensional sequence data mining methods.
Copyright (C) 2022, MIT license (this portion of code is subject to licensing from source project distribution)

Created in Dec, 2021
Copyright (C) 2024, License GPL Version 3 or superior (see LICENSE file)

Authors:
- Vanessa Lago Machado
- Tarlis Portela
- Lucas May Petry (adapted)
'''
# --------------------------------------------------------------------------------
import time
import pandas as pd
import numpy as np
import math
from datetime import datetime
from typing import List, Dict, Union
# --------------------------------------------------------------------------------
# Import class and data model
from matdata.preprocess import *
from matdata.dataset import *
from matmodel.base import *
from matmodel.descriptor import *

from matsimilarity.core import SimilarityMeasure

# --------------------------------------------------------------------------------
class MUITAS(SimilarityMeasure):
    """
    MUITAS: Similarity Measure for Multiple Aspect Trajectory

    This class provides methods to analyze and measure the similarity between multiple aspect trajectory data.

    Attributes:
        thresholds (Dict[int, float]): A dictionary to store threshold values for different attribute types.
        _parityT1T2 (float): Parity score from trajectory T1 to T2.
        _parityT2T1 (float): Parity score from trajectory T2 to T1.
        _data_descriptor (DataDescriptor): The data descriptor for the dataset.
        features (List[Feature]): A list to store features with their attributes and weights.
        _default_thresholds (Dict[str, float]): Default threshold values based on attribute types.
        
    References
    ----------
    `Petry, L. M., Ferrero, C. A., Alvares, L. O., Renso, C., & Bogorny, V.
    (2019). Towards Semantic-Aware Multiple-Aspect Trajectory Similarity
    Measuring. Transactions in GIS (accepted), XX(X), XXX-XXX.
    <https://onlinelibrary.wiley.com/journal/14679671>`__
    """
    def __init__(self, dataset_descriptor: DataDescriptor = None):
        """
        Initializes the MUITAS class with the given dataset descriptor.
        
        Args:
            dataset_descriptor (DataDescriptor, optional): The data descriptor for the dataset.
        """
        self.thresholds: Dict[int, float] = {}
        self._parityT1T2 = 0
        self._parityT2T1 = 0
        self._data_descriptor = dataset_descriptor
        self.features: List[Feature] = []
        # Default thresholds
        self._default_thresholds = {
            'space2d': 0.2, 
            'space3d': 0.2, 
            'time': 100,
            'numeric': 0.1
        }
        self._initialize_thresholds()

    @property
    def attributes(self):
        """
        Getter for attributes from the data descriptor.

        Returns:
            List[FeatureDescriptor]: List of attributes from the data descriptor.
        """
        return self._data_descriptor.attributes

    def add_feature(self, attributes: Union[List[int], List[FeatureDescriptor]], weight: float):
        """
        Add a feature to the MUITAS object. 

        Args:
            attributes (List[int] or List[FeatureDescriptor]): Attributes of a feature can be either a list of 
                indices or a list of FeatureDescriptor objects (following attributes in dataset descriptor)
            weight (float): The weight of the feature.
        """
        if isinstance(attributes, list) and all(isinstance(attr, FeatureDescriptor) for attr in attributes):
            aux_attributes: List[int] = [self.get_index_attribute(attr) for attr in attributes]
            attributes = aux_attributes
        feat = Feature(attributes, weight)
        print(f"Feature: {feat}")
        self.features.append(feat)

    def _initialize_thresholds(self):
        """
        Initialize thresholds for each attribute based on its type, using default threshold values.
        """
        for idx, attr in enumerate(self._data_descriptor.attributes):
            self.thresholds[idx] = self._default_thresholds.get(attr.dtype.lower(), 0)

    def set_threshold(self, att_type: str = None, threshold_value: Union[float, List[float]] = None):
        """
        Set the threshold value for a given aspect or list of aspects.

        Args:
            att_type (str, optional): The aspect type to set the threshold.
            threshold_value (float or list, optional): The threshold value to set or a list of threshold values.

        Raises:
            TypeError: If att_type is not a string or None.
            ValueError: If no threshold is provided for given aspect types in the list.
        """
        if att_type is None:
            if not isinstance(threshold_value, list):
                raise ValueError("Thresholds should be provided as a list for each individual attribute.")
            for idx, value_threshold in enumerate(threshold_value):
                self.thresholds[idx] = value_threshold
        elif isinstance(att_type, str):
            if not isinstance(threshold_value, float):
                raise ValueError("Threshold should be provided as a single float for the specified attribute type.")
            idx_att_type = self.get_indices_by_dtype(att_type)
            if not idx_att_type:
                raise ValueError(f"No attribute in dataset descriptor has the aspect type {att_type}.")
            for idx in idx_att_type:
                self.thresholds[idx] = threshold_value
        else:
            raise TypeError("att_type should be a string or None.")

    def similarity(self, t1: MultipleAspectSequence, t2: MultipleAspectSequence) -> float:
        """
        Compute the similarity between two multiple aspect sequences.

        Args:
            t1 (MultipleAspectSequence): The first multiple aspect trajectory or subtrajectory.
            t2 (MultipleAspectSequence): The second multiple aspect trajectory or subtrajectory.

        Returns:
            float: The computed similarity score.
        """
        self._parityT1T2 = 0
        self._parityT2T1 = 0
        len_t1 = len(t1.points)
        len_t2 = len(t2.points)
        self._normalize_weights()

        scores = [[0.0] * len_t2 for _ in range(len_t1)]
        
        for i in range(len_t1):
            max_score_row = 0
            for j in range(len_t2):
                scores[i][j] = self.score(t1.points[i], t2.points[j])
                max_score_row = max(max_score_row, scores[i][j])
            self._parityT1T2 += max_score_row

        for j in range(len_t2):
            max_score_col = 0
            for i in range(len_t1):
                max_score_col = max(max_score_col, scores[i][j])
            self._parityT2T1 += max_score_col
        
        return (self._parityT2T1 + self._parityT1T2) / (len_t1 + len_t2)

    def score(self, p1: Point = None, p2: Point = None) -> float:
        """
        Compute the score between two points based on their aspects and features.

        Args:
            p1 (Point, optional): The first point.
            p2 (Point, optional): The second point.

        Returns:
            float: The computed score.
        """
        score = 0
        for feat in self.features:
            tempMatch = 1  # Initialize as matched
            for idx in feat.attributes:
                a1 = p1.aspects[idx]
                a2 = p2.aspects[idx]
                attr = self._data_descriptor.attributes[idx]
                distance = attr.comparator.distance(a1, a2)
                threshold = self.thresholds.get(idx, 0)
                if distance > threshold:
                    tempMatch = 0  # Set as unmatched and break
                    break
            if tempMatch:
                score += feat.weight
        return score

    def get_indices_by_dtype(self, dtype: str) -> List[int]:
        """
        Get indices of attributes in the data descriptor where the attribute's dtype matches the given parameter.

        Args:
            dtype (str): The dtype to match.

        Returns:
            List[int]: A list of indices where the attribute's dtype matches the given parameter.
        """
        return [idx for idx, attr in enumerate(self._data_descriptor.attributes) if attr.dtype == dtype]

    def identify_unique_types_descriptor(self) -> set:
        """
        Identify unique types in the dataset descriptor attributes.

        Returns:
            set: A set of unique attribute types.
        """
        return {attr.dtype for attr in self._data_descriptor.attributes}

    def _normalize_weights(self):
        """
        Normalize the weights of features so that their sum equals 1.
        """
        total_weight = sum(feature.weight for feature in self.features)
        if total_weight > 0:
            for feature in self.features:
                feature.weight /= total_weight

    def get_index_attribute(self, attribute: FeatureDescriptor) -> int:
        """
        Get the index of an attribute in the data descriptor attributes.

        Args:
            attribute (FeatureDescriptor): The attribute to find the index for.

        Returns:
            int: The index of the attribute in the data descriptor attributes.
                 Returns -1 if the attribute is not found.
        """
        for idx, attr in enumerate(self._data_descriptor.attributes):
            if attribute == attr:
                return idx
        return -1

    def display_attributes_and_thresholds(self):
        """
        Display the attributes and their corresponding thresholds.
        """
        for idx, attr in enumerate(self._data_descriptor.attributes):
            print(f"Attribute: {attr.name}, Type: {attr.dtype}, Threshold: {self.thresholds.get(idx, 'Not set')}")


# ------------------------------------------------------------------------------------------------------------
# Feature object in MUITAS Application
# ------------------------------------------------------------------------------------------------------------
class Feature:
    """
    Feature: A class representing a feature in the MUITAS application.

    Attributes:
        _attributes (List[int]): A list of attribute indices.
        _weight (float): The weight of the feature.
    """
    def __init__(self, attributes: List[int], weight: float):
        """
        Initialize a Feature object.

        Args:
            attributes (List[int]): A list of attribute indices.
            weight (float): The weight of the feature.
        """
        self._attributes: List[int] = attributes
        self._weight = weight

    @property
    def attributes(self) -> List[int]:
        """Getter for attributes."""
        return self._attributes

    @attributes.setter
    def attributes(self, attributes: List[int]):
        """Setter for attributes."""
        self._attributes = attributes

    @property
    def weight(self) -> float:
        """Getter for weight."""
        return self._weight

    @weight.setter
    def weight(self, weight: float):
        """Setter for weight."""
        self._weight = weight

    def __str__(self) -> str:
        """String representation of Feature."""
        attribute_str = ', '.join(str(attr) for attr in self._attributes)
        return f"Attributes: [{attribute_str}], Weight: {self._weight}"
