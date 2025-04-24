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
# --------------------------------------------------------------------------------import numpy as np

# Import class and data model
from matmodel.base import *
from matmodel.descriptor import *

from matsimilarity.core import SimilarityMeasure

# --------------------------------------------------------------------------------
class MSM(SimilarityMeasure):
    """
    MSM: Multidimensional Similarity Measure.

    This class provides methods to analyze and measure the similarity between multiple aspect trajectory data.

    Attributes:
        TODO
        
    References
    ----------
    `Furtado, A. S., Kopanaki, D., Alvares, L. O., & Bogorny, V. (2016).
    Multidimensional similarity measuring for semantic trajectories.
    Transactions in GIS, 20(2), 280-298.
    <https://onlinelibrary.wiley.com/doi/abs/10.1111/tgis.12156>`__
    """
    def __init__(self, dataset_descriptor: DataDescriptor = None, weights = []):
        super().__init__(dataset_descriptor)
        
        if isinstance(weights, np.ndarray):
            weights_sum = weights.sum()
        else:
            weights = [1.0 for _ in self.attributes]
            weights_sum = sum(weights)
        weights = np.array(weights)
        self.weights = weights / weights_sum
    
    def similarity(self, t1: MultipleAspectSequence, t2: MultipleAspectSequence) -> float:
        """
        Compute the similarity between two multiple aspect sequences.

        Args:
            t1 (MultipleAspectSequence): The first multiple aspect trajectory or subtrajectory.
            t2 (MultipleAspectSequence): The second multiple aspect trajectory or subtrajectory.

        Returns:
            float: The computed similarity score.
        """
        matrix = np.zeros(shape=(t1.size, t2.size))

        for i, p1 in enumerate(t1.points):
            matrix[i] = [self._score(p1, p2) for p2 in t2.points]

        parity1 = matrix.max(axis=1).sum()
        parity2 = matrix.max(axis=0).sum()
        return (parity1 + parity2) / (t1.size + t2.size)

    def _score(self, p1: Point = None, p2: Point = None) -> float:
        matches = np.zeros(len(self.attributes))
        for idx, _ in enumerate(self.attributes):
            a1 = p1.aspects[idx]
            a2 = p2.aspects[idx]
            attr = self._data_descriptor.attributes[idx]
            threshold = self.thresholds.get(idx, 0)
            distance = attr.comparator.distance(a1, a2)
            matches[idx] = distance <= threshold
        return sum(matches * self.weights)