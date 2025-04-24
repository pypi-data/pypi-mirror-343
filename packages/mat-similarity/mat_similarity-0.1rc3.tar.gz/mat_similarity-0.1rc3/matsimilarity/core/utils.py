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
from joblib import Parallel, delayed
from sklearn.utils import gen_even_slices

from tqdm.auto import tqdm

def similarity_matrix(A, B=None, measure=None, n_jobs=1):
    """
    Computes the similarity matrix from a list of trajectories Ta x Ta, or Ta x Tb (if provided).
    
    Parameters:
    -----------
    A : list of MultipleAspectSequence
        List of Trajectory objects to compute similarity from. Each trajectory should be a MultipleAspectSequence.
    B : list of MultipleAspectSequence (optional)
        List of Trajectory objects to compute similarity to `A`. Each trajectory should be a MultipleAspectSequence.
    measure : SimilarityMeasure instance
        A class with a similarity function that takes two trajectories and returns a similarity score.
    n_jobs : int, optional
        The number of parallel jobs to use for computation (default is 1).
    
    Returns:
    --------
    np.ndarray : similarity array with shape (len(A), len(B)).
        A 2D numpy array containing similarity scores between trajectories. 
        The element at [i, j] represents the similarity between trajectory A[i] and B[j].
    
    Example:
    --------
    >>> T = [Trajectory1, Trajectory2, Trajectory3]
    >>> sim_matrix = similarity_matrix(T, measure=MUITAS(), n_jobs=4)
    >>> print(sim_matrix)
    [[1.0, 0.8, 0.3],
     [0.8, 1.0, 0.5],
     [0.3, 0.5, 1.0]]
     
    
    Source:
    -----------
    From trajminer with MIT License:
    https://github.com/trajminer/trajminer/blob/master/trajminer/similarity/pairwise.py
    """
    def compute_slice(A, B, s):
        matrix = np.zeros(shape=(len(A), len(B)))

        for i in tqdm(range(s.start + 1, len(A)), desc='Computing similarity matrix'):
            for j in range(0, min(len(B), i - s.start)):
                matrix[i][j] = measure.similarity(A[i], B[j])
        return matrix

    upper = B is not None
    B = A if not B else B
    func = delayed(compute_slice)

    similarity = Parallel(n_jobs=n_jobs, verbose=0)(
        func(A, B[s], s) for s in gen_even_slices(len(B), n_jobs))
    similarity = np.hstack(similarity)

    if not upper:
        similarity += similarity.transpose() + np.identity(len(A))

    return similarity