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
import numpy as np

# Import class and data model
from matmodel.base import *
from matmodel.descriptor import *

from matsimilarity.core import SimilarityMeasure

# --------------------------------------------------------------------------------
class LCSS(SimilarityMeasure):
    """
    LCSS: Longest Common SubSequence.

    This class provides methods to analyze and measure the similarity between multiple aspect trajectory data.

    Attributes:
        TODO
        
    References
    ----------
    `Vlachos, M., Kollios, G., & Gunopulos, D. (2002). Discovering similar
    multidimensional trajectories. In Data Engineering, 2002. Proceedings.
    18th International Conference on (pp. 673-684). IEEE.
    <https://ieeexplore.ieee.org/abstract/document/994784/>`__
    """
    def __init__(self, dataset_descriptor: DataDescriptor = None):
        super().__init__(dataset_descriptor)
    
    def similarity(self, t1: MultipleAspectSequence, t2: MultipleAspectSequence) -> float:
        """
        Compute the similarity between two multiple aspect sequences.

        Args:
            t1 (MultipleAspectSequence): The first multiple aspect trajectory or subtrajectory.
            t2 (MultipleAspectSequence): The second multiple aspect trajectory or subtrajectory.

        Returns:
            float: The computed similarity score.
        """
        matrix = np.zeros(shape=[2, t2.size + 1])

        for i, p1 in enumerate(t1.points):
            ndx = i & 1
            ndx1 = int(not ndx)
            for j, p2 in enumerate(t2.points):
                if self._match(p1, p2):
                    matrix[ndx1][j+1] = matrix[ndx][j] + 1
                else:
                    matrix[ndx1][j+1] = max(matrix[ndx1][j], matrix[ndx][j+1])

        return matrix[1][t2.size] / min(t1.size, t2.size)

    def _match(self, p1: Point = None, p2: Point = None) -> int:
        for idx, _ in enumerate(self.attributes):
            a1 = p1.aspects[idx]
            a2 = p2.aspects[idx]
            attr = self._data_descriptor.attributes[idx]
            distance = attr.comparator.distance(a1, a2)
            threshold = self.thresholds.get(idx, 0)
            if distance > threshold:
                break
        else:
            return 0
        return 1