import numpy as np


def cosine_similarity(x, y, a):
    x = np.array(x.tolist())
    y = np.array(y.tolist())
    ax = np.dot(a, x.T)
    ay = np.dot(a, y.T)
    ax_norm = np.linalg.norm(ax, axis=0)
    ay_norm = np.linalg.norm(ay, axis=0)
    return np.diagonal(np.dot(ax.T, ay)) / (ax_norm * ay_norm)