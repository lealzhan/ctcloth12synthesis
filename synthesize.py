import numpy as np


def findMaximumConsistencyPixels(S, W, w_r, w_c):
    K, e_h, e_w = S.shape
    t_h, t_w = W.shape

    max_cons = 0
    pixels = []

    for u in range(0, K):
        A = S[u]
        for r in range(0, e_h):
            for c in range(0, e_w):
                cur_cons = 0
                if A[r, c] == W[w_r, w_c]:
                    cur_cons = 1
                    if r > 0 and w_r > 0 and A[r-1, c] == W[w_r-1, w_c]:
                        cur_cons += 1
                    if r < e_h-1 and w_r < t_h-1 and A[r+1, c] == W[w_r+1, w_c]:
                        cur_cons += 1
                    if c > 0 and w_c > 0 and A[r, c-1] == W[w_r, w_c-1]:
                        cur_cons += 1
                    if c < e_w-1 and w_c < t_w-1 and A[r, c+1] == W[w_r, w_c+1]:
                        cur_cons += 1

                if cur_cons > max_cons:
                    max_cons = cur_cons
                    pixels = [[u, r, c]]
                elif cur_cons == max_cons:
                    pixels.append([u, r, c])

    return pixels


def structAwareSynthesize(S, W):
    ''' Parameters:
    S: (k, e_h, e_w), boolean. weave patterns of k example
    W: (t_h, t_w), boolean. target pattern
    And,
    K: k examples
    C: (t_h, t_w, 3), integer. C(i,j) = (u, r, c), u represents example id
    '''
    K, e_h, e_w = S.shape
    t_h, t_w = W.shape
    C = np.zeros((t_h, t_w, 3), dtype='int32')

    for c in range(0, t_w):
        # initialize parameters in first row of one column
        t0s = findMaximumConsistencyPixels(S, W, 0, c)
        f0_t = [0] * len(t0s)
        cnt_t_id = [-1] * len(t0s)

        cns_ts = [t0s]
        cnt_t_ids = [cnt_t_id]

        # compute f_t using dynamic programming in up-down order
        # save cns_ts and cnt_t_ids for computing final ts
        for r in range(1, t_h):
            t1s = findMaximumConsistencyPixels(S, W, r, c)
            f1_t = [0] * len(t1s)
            cnt_t_id = [-1] * len(t1s)

            for (i, t1) in zip(range(len(t1s)), t1s):
                for (j, t0) in zip(range(len(t0s)), t0s):
                    gain = 0
                    if (t1[0] == t0[0] and t1[1] == t0[1] + 1 and t1[2] == t0[2]):
                        gain = 1
                    if f0_t[j] + gain > f1_t[i]:
                        f1_t[i] = f0_t[j] + gain
                        cnt_t_id[i] = j

            cns_ts.append(t1s)
            cnt_t_ids.append(cnt_t_id)
            t0s = t1s
            f0_t = f1_t

        # the maximum continutiy is the maximum one in f_t in final row
        t_id = 0
        max_cnt = f0_t[0]
        for i in range(0, len(f0_t)):
            if f0_t[i] > max_cnt:
                max_cnt = f0_t
                t_id = i

        # find the best ts by solving the maximum column continuity of the column in bottom-up order
        order = range(0, t_h)
        order.reverse();
        for i in order:
            C[i, c] = cns_ts[i][t_id]
            t_id = cnt_t_ids[i][t_id]

    return C


if __name__ == '__main__':
    pass
