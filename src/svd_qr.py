import numpy as np


def svd(matrix):
    # BIKIN AT*A
    A = matrix.transpose() @ matrix

    # QR ALGORITHM AT*A untuk konvergen mendapatkan eigenvalue A dan eigenvector V
    for i in range(1):
        # DIGUNAKAN BUILT-IN FUNGSI QR DECOMPOSITION, asumsi boleh karena tidak langsung menghasilkan SVD
        Q, R = np.linalg.qr(A)
        A = R @ Q
        if not i:   # iterasi pertama inisialisasi V dengan Q
            V = Q
        else:
            V = V @ Q   # iterasi selanjutnya V = Q1 * Q2 ... * QN

    # DAPATKAN SIGMA
    sigma = np.diag(np.clip(np.sqrt(np.absolute(np.diagonal(A))), 1e-4,np.Inf))

    # Hitung inv(sigma) untuk menemukan U
    invsigma = np.linalg.inv(sigma)

    # U dari U = A * V * inv(S),  dapat asumsi V^T^-1 = V karena V orthogonal
    U = (matrix @ V) @ invsigma

    # TRANSPOSE V
    V = np.transpose(V)

    return U, sigma, V


# TO PROCESSS THE DIFFERENT COLOR CHANNELS
# SUPPORT L, LA, RGB, RGBA, CMYK
# P and PA needs to be converted to RGB first
def matriximage(colormatrix, rank):
    m = colormatrix.shape[0]
    n = colormatrix.shape[1]
    col_channels = colormatrix.shape[2]

    imgO = np.zeros([m,n,col_channels])

    if col_channels > 0:
        c1 = np.array([[colormatrix[i][j][0] for j in range(n)] for i in range(m)]).astype(int)
        c11, c12, c13 = svd(c1)
        c11_ranked = c11[:, 0:rank]
        c12_ranked = c12[0:rank,0:rank]
        c13_ranked = c13[0:rank, :]
        c1_f = np.clip(((c11_ranked @ c12_ranked) @ c13_ranked).round(0), 0, 255)
        imgO[:,:,0] = c1_f
    if col_channels > 1:
        c2 = np.array([[colormatrix[i][j][1] for j in range(n)] for i in range(m)]).astype(int)
        c21, c22, c23 = svd(c2)
        c21_ranked = c21[:, 0:rank]
        c22_ranked = c22[0:rank,0:rank]
        c23_ranked = c23[0:rank, :]
        c2_f = np.clip(((c21_ranked @ c22_ranked) @ c23_ranked).round(0), 0, 255)
        imgO[:,:,1] = c2_f
    if col_channels > 2:
        c3 = np.array([[colormatrix[i][j][2] for j in range(n)] for i in range(m)]).astype(int)
        c31, c32, c33 = svd(c3)
        c31_ranked = c31[:, 0:rank]
        c32_ranked = c32[0:rank,0:rank]
        c33_ranked = c33[0:rank, :]
        c3_f = np.clip(((c31_ranked @ c32_ranked) @ c33_ranked).round(0), 0, 255)
        imgO[:,:,2] = c3_f
    if col_channels > 3:
        c4 = np.array([[colormatrix[i][j][3] for j in range(n)] for i in range(m)]).astype(int)
        c41, c42, c43 = svd(c4)
        c41_ranked = c41[:, 0:rank]
        c42_ranked = c42[0:rank,0:rank]
        c43_ranked = c43[0:rank, :]
        c4_f = np.clip(((c41_ranked @ c42_ranked) @ c43_ranked).round(0), 0, 255)
        imgO[:,:,3] = c4_f

    return np.uint8(imgO)
