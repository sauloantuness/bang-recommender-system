import numpy as np
from numpy.random import rand
from pprint import pprint


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

def test_gd():
    x = np.array([
        [0],
        [1],
        [2],
        [3],
        [4],
    ])

    y = np.array([
        0,
        4,
        8,
        12,
        16,
    ])
    

    theta = gradient_descent(x, y)
    print (theta)

def test_filmes():

    theta_usuarios = [
        [rand(), rand()],
        [rand(), rand()],
        [rand(), rand()],
        [rand(), rand()],
    ]

    theta_filmes = [
        [None, None],
        [None, None],
        [None, None],
        [None, None],
    ]

    # linha filme
    # coluna usuario

    ratings = [
        [1,1,0,0],
        [1,1,0,0],
        [0,0,1,1],
        [0,0,1,1],
    ]

    ratings_t = np.transpose(ratings).tolist()

    nr_usuarios = len(theta_usuarios)
    nr_filmes = len(theta_filmes)
    
    i = 0
    while i < 1000:
        i += 1

        for filme in range(nr_filmes):
            x = np.array(
                theta_usuarios
            )

            y = np.array(
                ratings[filme]
            )

            theta_filmes[filme] = gradient_descent(x, y)[1:]


        for usuario in range(nr_usuarios):
            x = np.array(
                theta_filmes
            )

            y = np.array(
                ratings_t[usuario]
            )

            theta_usuarios[usuario] = gradient_descent(x, y)[1:]

        print('Theta Usuarios')
        pprint(theta_usuarios)

        print('')
        print('Theta Filmes')
        pprint(theta_filmes)
        print('\n\n')

if __name__ == '__main__':
    test_filmes()
