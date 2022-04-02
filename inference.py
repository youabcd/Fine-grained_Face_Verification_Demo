import numpy as np
from utils.LBP import local_bp
from utils.cosine_similarity import cosine_similarity


def inference(img1, img2, parameter, feature):
    img1 = local_bp(img1)
    img2 = local_bp(img2)
    feature = np.load(feature, allow_pickle=True)['feature'].item()
    feature_pca = feature['feature_pca']
    img1 = (feature_pca @ img1[:, np.newaxis]).reshape(-1)
    img2 = (feature_pca @ img2[:, np.newaxis]).reshape(-1)
    img1 = img1 / np.linalg.norm(img1)
    img2 = img2 / np.linalg.norm(img2)
    parameter = np.load(parameter, allow_pickle=True)['parameter'].item()
    a = parameter['a0_s'][0]
    theta = parameter['best_theta'][0]
    img1 = img1[:a.shape[1]]
    img2 = img2[:a.shape[1]]
    cs = cosine_similarity(img1.reshape((1, -1)), img2.reshape((1, -1)), a)[0]
    print(cs)
    if cs >= theta:
        print("same")
        res = "same"
    else:
        print("twins")
        res = "twins"
    return res, cs
