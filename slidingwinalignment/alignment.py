import numpy as np
from typing import List, Dict, Tuple

def transform_similarity_matrix(matrix, midpoint=0.5, sharpness=10, scale=10):
    # Normalize to [-1, 1]
    matrix = 2 * (matrix - matrix.min()) / (matrix.max() - matrix.min()) - 1
    # Apply sigmoid transformation
    def sigmoid_reward(x):
        return scale * (1 / (1 + np.exp(-sharpness * (x - midpoint))) - 0.5) * 2
    return np.vectorize(sigmoid_reward)(matrix)

def OutputLCS(back, i, j):
    if i == 0 and j == 0:
        return [], []
    if back[(i,j)] == '0':
        return [], []
    elif back[(i,j)] == 'd':
        o1,o2 = OutputLCS(back, i - 1, j)
        return o1+[str(i-1)], o2+['-']
    elif back[(i,j)] == 'r':
        o1,o2 = OutputLCS(back, i, j - 1)
        return o1+['-'], o2+[str(j-1)]
    elif back[(i,j)] == 'm':
        o1,o2 = OutputLCS(back, i - 1, j - 1)
        return o1+[str(i-1)], o2+[str(j-1)]

def local_alignment(match_reward: List[list[int]], indel_penalty: int) -> Tuple[int, str, str]:
    v, w = len(match_reward), len(match_reward[0])
    s = {}
    s[(0,0)] = 0
    back = {}
    for i in range(1, v+1):
        s[(i,0)] = max(s[(i-1,0)]-indel_penalty,0)
        if s[(i,0)] == s[(i-1,0)]-indel_penalty:
            back[(i,0)] = 'd'
        else:
            back[(i,0)] = '0'
    for j in range(1, w+1):
        s[(0,j)] = max(s[(0,j-1)]-indel_penalty,0)
        if s[(0,j)] == s[(0,j-1)]-indel_penalty:
            back[(0,j)] = 'r'
        else:
            back[(0,j)] = '0'
    for i in range(1, v+1):
        for j in range(1, w+1):
            s[(i,j)] = max(s[(i-1,j)]-indel_penalty,s[(i,j-1)]-indel_penalty,s[(i-1,j-1)]+match_reward[i-1][j-1],0)
            if s[(i,j)] == s[(i-1,j)]-indel_penalty:
                back[(i,j)] = 'd'
            elif s[(i,j)] == s[(i,j-1)]-indel_penalty:
                back[(i,j)] = 'r'
            elif s[(i,j)] == s[(i-1,j-1)]+match_reward[i-1][j-1]:
                back[(i,j)] = 'm'
            else:
                back[(i,j)] = '0'

    bestscore = max(s.values())

    for i in range(v+1):
        for j in range(w+1):
            if s[(i,j)] == bestscore:
                o1,o2 = OutputLCS(back, i, j)
    
                return bestscore,[o1[0],o1[-1]],[o2[0],o2[-1]]