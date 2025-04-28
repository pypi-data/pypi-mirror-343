import numpy as np
from logme import LogME


def logme_icml(
    f: np.array,
    y: np.array,
    start_alpha: float = 1,
    start_beta: float = 1,
    max_iterations: int = 10,
    tol=1e-5,
) -> float:
    n, d = f.shape
    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    k = y.shape[1]

    svd_output = np.linalg.svd(f.T @ f)
    # print(svd_output)
    v = svd_output.U
    sigma = svd_output.S
    scores = []
    for k_ in range(k):
        y_ = y[:, k_]  # .reshape(-1, 1)

        alpha = start_alpha
        beta = start_beta

        for i in range(max_iterations):
            prev_alpha = alpha
            prev_beta = beta

            gamma = (beta * sigma / (alpha + beta * sigma)).sum()
            lambda_inv = np.diag((alpha + beta * sigma) ** -1)
            m = beta * v @ lambda_inv @ v.T @ f.T @ y_

            alpha = gamma / m.T.dot(m)
            beta = (n - gamma) / np.linalg.norm(f @ m - y_) ** 2

            if np.abs(alpha - prev_alpha) < tol and np.abs(beta - prev_beta) < tol:
                break

        a = alpha * np.eye(d) + beta * f.T @ f
        score = (
            n * 0.5 * np.log(beta)
            + d * 0.5 * np.log(alpha)
            - n * 0.5 * np.log(2 * np.pi)
            - beta * 0.5 * np.linalg.norm(f @ m - y_) ** 2
            - alpha * 0.5 * m.T.dot(m)
            - 0.5 * np.log(np.linalg.det(a))
        ) / n
        scores.append(score)

    return sum(scores) / len(scores)


# copied from LogME implementation
def truncated_svd(x):
    u, s, vh = np.linalg.svd(x.transpose() @ x)
    s = np.sqrt(s)
    u_times_sigma = x @ vh.transpose()
    k = np.sum((s > 1e-10) * 1)  # rank of f
    s = s.reshape(-1, 1)
    s = s[:k]
    vh = vh[:k]
    u = u_times_sigma[:, :k] / s.reshape(1, -1)
    return u, s, vh


def logme_fixed_point(
    f: np.array,
    y: np.array,
    start_alpha: float = 1,
    start_beta: float = 1,
    max_iterations: int = 10,
    tol=1e-3,
) -> float:
    epsilon = 1e-5
    n, d = f.shape

    if len(y.shape) == 1:
        y = y.reshape(-1, 1)
    k = y.shape[1]

    u, s, vh = truncated_svd(f)
    s2 = (s**2).flatten()
    # r = u.shape[1]
    # print(svd_output)
    scores = []
    for k_ in range(k):
        y_ = y[:, k_]  # .reshape(-1, 1)
        z = u.T @ y_
        z2 = z**2
        # print(f"{z.sum()}")
        delta = (y_**2).sum() - (z**2).sum()
        # print(f"{delta=}")

        alpha = start_alpha
        beta = start_beta
        t = alpha / beta

        for i in range(max_iterations):
            m2 = (s2 * z2 / (t + s2) ** 2).sum()
            # print(f"{m2=}")
            gamma = (s2 / (t + s2)).sum()
            # print(f"{gamma=}")
            # print(f"{z2=}")
            # print(f"{s2.sum()=}")
            res2 = (z2 / (1 + s2 / t) ** 2).sum() + delta
            # print(f"{z2 / (1 + s2 / t)**2=}")
            # print(f"{res2=}")

            alpha = gamma / (m2 + epsilon)
            beta = (n - gamma) / (res2 + epsilon)

            t_new = alpha / beta

            if np.abs(t_new - t) < tol:
                break

        # m = vh.T @ np.diag((s / (t + s)).flatten()) @ z

        a = alpha * np.eye(d) + beta * f.T @ f
        # print(f"{alpha=}")
        # print(f"{beta=}")
        # print(f"{gamma=}")
        score = (
            n * 0.5 * np.log(beta)
            + d * 0.5 * np.log(alpha)
            - n * 0.5 * np.log(2 * np.pi)
            - beta * 0.5 * res2
            - alpha * 0.5 * m2
            - 0.5 * np.log(np.linalg.det(a))
        ) / n

        scores.append(score)

    return sum(scores) / len(scores)


def main():
    f = np.random.rand(20, 3)
    y = np.ones(20)
    y[:5] = 0
    np.random.shuffle(y)

    score_icml = logme_icml(f, y)
    score_fixed = logme_fixed_point(f, y)

    lm = LogME(regression=True)
    score = lm.fit(f, y)

    a = 1


if __name__ == "__main__":
    main()
