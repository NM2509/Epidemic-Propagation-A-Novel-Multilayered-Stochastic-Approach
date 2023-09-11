##################################################################
# Re-writing cumulative function using numba for time efficiency #
##################################################################

@jit(nopython=True, fastmath=True)
def cumsum_numba(a):
    out = np.empty_like(a)
    cumsum = 0
    for i in range(a.shape[0]):
        cumsum += a[i]
        out[i] = cumsum
    return out
