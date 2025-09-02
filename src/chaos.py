import numpy as np, pandas as pd
from statsmodels.tsa.stattools import bds
from scipy.spatial.distance import pdist, squareform

# --- Hurst (R/S simplificado) ---
def hurst_rs(x):
    x = np.asarray(x, float)
    N = len(x)
    if N < 100: return np.nan
    max_k = int(np.floor(N/2))
    ks = np.unique(np.floor(np.logspace(1, np.log10(max_k), 20)).astype(int))
    RS = []
    for k in ks:
        n = N // k
        if n < 2: continue
        X = x[:n*k].reshape(n, k)
        Y = X - X.mean(axis=1, keepdims=True)
        Z = np.cumsum(Y, axis=1)
        R = Z.max(axis=1) - Z.min(axis=1)
        S = X.std(axis=1, ddof=1)
        RS_k = np.mean(R / (S + 1e-12))
        RS.append((k, RS_k))
    ks, RS = np.array(RS).T
    H = np.polyfit(np.log(ks), np.log(RS), 1)[0]
    return H

# --- BDS test sobre retornos ---
def bds_test(x, m=2, eps=None):
    x = np.asarray(x, float)
    if eps is None:
        eps = 0.7*np.std(x)  # regla práctica
    res = bds(x, m=m, epsilon=eps)
    # statsmodels retorna una tupla por cada m si le pasas lista;
    # aquí usamos un m único: devuelve objeto con .statistic y .pvalue
    return {"stat": res.statistic, "pvalue": res.pvalue, "m": m, "eps": eps}

# --- Lyapunov (Rosenstein) sobre serie escalar ---
def lyapunov_rosenstein(x, emb_dim=6, tau=1, mean_period=10):
    """
    Aproximación del LCE máximo (Rosenstein et al. 1993).
    x: serie escalar (retornos o precio)
    emb_dim: dimensión de incrustación
    tau: retardo
    mean_period: excluir vecinos más cercanos en tiempo (Theiler window)
    """
    x = np.asarray(x, float)
    N = len(x) - (emb_dim-1)*tau
    if N < 200: return np.nan
    Y = np.column_stack([x[i:i+N] for i in range(0, emb_dim*tau, tau)])
    D = squareform(pdist(Y))
    # Excluir vecindad temporal
    for i in range(N):
        D[i, max(0, i-mean_period):i+mean_period+1] = np.inf
    nn = np.argmin(D, axis=1)
    # Divergencia media
    max_t = min(100, N-1)
    div = []
    for j in range(1, max_t):
        idx = np.arange(N-j)
        d = np.linalg.norm(Y[idx+j] - Y[nn[idx]+j], axis=1)
        d0 = np.linalg.norm(Y[idx]   - Y[nn[idx]], axis=1)
        valid = (d0 > 0) & np.isfinite(d) & (d>0)
        if valid.sum() < 10: break
        div.append(np.mean(np.log(d[valid]) - np.log(d0[valid])))
    if len(div) < 5: return np.nan
    t = np.arange(1, 1+len(div))
    lce = np.polyfit(t, div, 1)[0]  # pendiente ~ LCE
    return lce
