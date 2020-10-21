import numpy as np
import random


def scalar_product(a, b):
    result = 0
    for i in range(len(a)):
        result += a[i] * b[i]
    return result


def SMAPE(X, Y, w):
    result = 0
    for i in range(len(X)):
        y_predict = scalar_product(X[i], w)
        y_real = Y[i]
        result += abs(y_predict - y_real) / (abs(y_predict) + abs(y_real))
    return result * 200 / len(X)


def LSM(X, Y, tau):
    return np.linalg.pinv(np.add(X.T.dot(X), np.cov(X.T).dot(tau))).dot(X.T).dot(Y)


def MSE(predict, real):
    return (predict - real) ** 2


def MSE_derivative(predict, real):
    return 2 * (predict - real)


def initialise_Q(X, Y, w):
    Q = 0
    for i in range(len(X)):
        Q += MSE(scalar_product(X[i], w), Y[i])
    return Q / len(X)


def initialise_weights(features, objects):
    w = np.zeros(features)
    for i in range(features):
        w[i] = random.uniform(-0.5 / objects, 0.5 / objects)
    return w


def SGD(X, Y, tau, iterations_limit=2000):
    objects, features = len(X), len(X[0])
    w = initialise_weights(features, objects)
    Q = initialise_Q(X, Y, w)
    iterations = 0
    while True:
        iterations += 1
        k = random.randint(0, objects - 1)
        x, y = X[k], Y[k]
        predict = scalar_product(x, w)
        loss_value = MSE(predict, y) + 0.5 * tau * np.linalg.norm(w)
        print("predict =", predict, "real =", y)
        learning_rate = 0.005
        for i in range(features):
            gradient = MSE_derivative(predict, y) * x[i]
            w[i] = w[i] * (1 - learning_rate * tau) - learning_rate * gradient
        decay = 0.05
        Q_previous = Q
        Q = (1 - decay) * Q + decay * loss_value
        if iterations == iterations_limit or abs(Q - Q_previous) < 0.001:
            break
    return w


def find_optimal_tau(X, Y, algorithm):
    tau_values = [10 ** -i for i in range(0, 10)]
    optimal_tau, optimal_w, min_smape = 0, [], 200
    for tau in tau_values:
        w = algorithm(X, Y, tau)
        smape = SMAPE(X, Y, w)
        if smape < min_smape:
            optimal_tau, optimal_w, min_smape = tau, w, smape
    return optimal_tau, optimal_w, min_smape


def process_file(filename):
    with open(filename) as file:
        features = int(next(file))
        objects_train = int(next(file))
        X_train = np.zeros((objects_train, features))
        Y_train = np.zeros(objects_train)
        for i in range(objects_train):
            line = [int(x) for x in next(file).split()]
            Y_train[i] = line.pop()
            X_train[i] = line
        objects_test = int(next(file))
        X_test = np.zeros((objects_test, features))
        Y_test = np.zeros(objects_test)
        for i in range(objects_test):
            line = [int(x) for x in next(file).split()]
            Y_test[i] = line.pop()
            X_test[i] = line
        return X_train, Y_train, X_test, Y_test


X_train, Y_train, X_test, Y_test = process_file("datasets/8.txt")
# optimal_tau_train, optimal_w_train, min_smape_train = find_optimal_tau(X_train, Y_train, LSM)
# print("optimal tau train =", optimal_tau_train, "\tmin smape train =", min_smape_train)
# print("smape test =", SMAPE(X_test, Y_test, optimal_w_train))
w = SGD(X_train, Y_train, 0.01)
