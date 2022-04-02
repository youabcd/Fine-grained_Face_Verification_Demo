import cv2
import numpy as np

uniform_lbp = [0, 1, 2, 3, 4, 6, 7, 8, 12, 14, 15, 16, 24, 28, 30, 31, 32, 48, 56, 60, 62, 63, 64, 96, 112, 120, 124,
               126, 127, 128, 129, 131, 135, 143, 159, 191, 192, 193, 195, 199, 207, 223, 224, 225, 227, 231, 239, 240,
               241, 243, 247, 248, 249, 251, 252, 253, 254, 255]


# 灰度值
def intensity(path: str):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = img.reshape([-1])
    return img


# 二进制转十进制
def bin_to_decimal(bin_array):
    res = 0
    bit_num = 0
    for i in bin_array:
        res += i << bit_num
        bit_num += 1
    return res


def cal_basic_lpb(padding):
    lbp = np.zeros(256, )
    uni_lbp = np.zeros((len(uniform_lbp) + 1))
    for i in range(1, 9):
        for j in range(1, 9):
            bin_array = []
            if padding[i - 1][j - 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i - 1][j] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i - 1][j + 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i][j + 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i + 1][j + 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i + 1][j] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i + 1][j - 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            if padding[i][j - 1] >= padding[i][j]:
                bin_array.append(1)
            else:
                bin_array.append(0)
            lbp[bin_to_decimal(bin_array=bin_array)] += 1
    lbp = lbp / ((padding.shape[0] - 2) * (padding.shape[1] - 2))
    uni_lbp[:len(uniform_lbp)] = lbp[uniform_lbp]
    uni_lbp[-1] = 1 - sum(lbp[uniform_lbp])
    return uni_lbp


# 获取跳变次数
def get_hop_times(n):
    count = 0
    binary_code = '{:08b}'.format(n)
    for x in range(8):
        if binary_code[x] != binary_code[(x + 1) % 8]:
            count += 1
    return count


# uniform LBP
def local_bp(path):
    if isinstance(path, str):
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = path
    uni_lbp = []
    for i in range(0, img.shape[0], 8):
        for j in range(0, img.shape[1], 8):
            local_img = img[i:i + 8, j:j + 8]
            padding = np.pad(local_img, ((1, 1), (1, 1)), 'constant', constant_values=(0, 0))
            uni_lbp.append(cal_basic_lpb(padding=padding))
    uni_lbp = np.array(uni_lbp).reshape(-1)
    return uni_lbp


if __name__ == '__main__':
    local_bp('../face_data/temp/face1.jpg')
    # uniform_lbp = []
    # for i in range(256):
    #     count = get_hop_times(n=i)
    #     if count <= 2:
    #         uniform_lbp.append(i)
    # print(uniform_lbp)
