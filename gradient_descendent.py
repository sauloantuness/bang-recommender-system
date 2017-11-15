import numpy as np

# http://www.bogotobogo.com/python/python_numpy_batch_gradient_descent_algorithm.php
def gradient_descent(x, y, alpha=0.01, nr_iterations=1000):

    # m - número de amostras
    # n - número features
    m, n = x.shape

    # Insere coluna theta zero = 1
    x = np.c_[ np.ones(m), x]

    theta = np.ones(n + 1)
    x_transpose = x.transpose()

    for iter in range(0, nr_iterations):
        hypothesis = np.dot(x, theta)
        loss = hypothesis - y
        J = np.sum(loss ** 2) / (2 * m)
        gradient = np.dot(x_transpose, loss) / m         
        theta = theta - alpha * gradient

    return theta