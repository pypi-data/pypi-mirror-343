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
import numpy as np

# Import class and data model
from matmodel.base import *
from matmodel.descriptor import *

from matsimilarity.core import SimilarityMeasure

# --------------------------------------------------------------------------------
class EDR(SimilarityMeasure):
    """
    EDR: Edit Distance on Real sequence

    This class provides methods to analyze and measure the similarity between multiple aspect trajectory data.

    Attributes:
        TODO
        
    References
    ----------
    `Chen, L., Özsu, M. T., & Oria, V. (2005, June). Robust and fast
    similarity search for moving object trajectories. In Proceedings
    of the 2005 ACM SIGMOD international conference on Management of
    data (pp. 491-502). ACM. <https://dl.acm.org/citation.cfm?id=1066213>`__
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
        matrix = np.zeros(shape=[t1.size + 1, t2.size + 1])
        matrix[:, 0] = np.r_[0:t1.size+1]
        matrix[0] = np.r_[0:t2.size+1]

        for i, p1 in enumerate(t1.points):
            for j, p2 in enumerate(t2.points):
                cost = self._match(p1, p2)
                matrix[i+1][j+1] = min(matrix[i][j] + cost,
                                       min(matrix[i+1][j] + 1,
                                           matrix[i][j+1] + 1))

        return 1 - matrix[t1.size][t2.size] / max(t1.size, t2.size)

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