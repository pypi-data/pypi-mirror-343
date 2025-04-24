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
'''
# --------------------------------------------------------------------------------
from typing import Dict
from abc import ABC, abstractmethod

from matmodel.base import *
from matmodel.descriptor import *

class SimilarityMeasure(ABC):
    
    def __init__(self, dataset_descriptor: DataDescriptor = None):
        
        self.thresholds: Dict[int, float] = {}
        self._data_descriptor = dataset_descriptor
        
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
    
    def _initialize_thresholds(self):
        """
        Initialize thresholds for each attribute based on its type, using default threshold values.
        """
        for idx, attr in enumerate(self._data_descriptor.attributes):
            self.thresholds[idx] = self._default_thresholds.get(attr.dtype.lower(), 0)

    def similarity(self, t1: MultipleAspectSequence, t2: MultipleAspectSequence) -> float:
        """Computes the similarity score of the given MAT.

        Parameters
        ----------
        t1 : MultipleAspectSequence instance of the trajectory 1.
        t2 : MultipleAspectSequence instance of the trajectory 2.

        Returns
        -------
        score : float
            Similarity score (between 0 and 1).
        """
        pass