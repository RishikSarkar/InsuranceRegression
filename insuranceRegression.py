import numpy as np
# from numpy import genfromtxt
import pandas as pd

# data = genfromtxt('multiTest1.csv', delimiter=',', dtype='float', skip_header=1)


'''
Read data from "insurance.csv," modify data to float, and convert to NumPy array
'''


file_handler = open("insurance.csv", "r")
data = pd.read_csv(file_handler, sep=",")
file_handler.close()

sex = {'male': 0., 'female': 1.}
data.sex = [sex[item] for item in data.sex]

smoker = {'no': 0., 'yes': 1.}
data.smoker = [smoker[item] for item in data.smoker]

region = {'southwest': 0., 'southeast': 1., 'northwest': 2., 'northeast': 3.}
data.region = [region[item] for item in data.region]

df = pd.DataFrame(data)

df['age'] = df['age'].astype(float)
df['children'] = df['children'].astype(float)

data = np.array(data)

# print(data)

x = np.array(data[:, :-1])
# print(x)
x_copy = x.copy()
y = np.array(data[:, -1])
# print(y)
cols = len(x[0])
# print(cols)

min_bias = np.min(y)
print(min_bias)


'''
Downscale relevant features in training data to 0 - 1 range
'''


def feature_scaling():
    for i in range(cols):
        maxx = np.max(x[:, i])
        x[:, i] = x[:, i] / maxx
        # meanx = np.mean(x[:, i])
        # stdx = np.std(x[:, i])
        # x[:, i] = (x[:, i] - meanx) / stdx
    # maxy = np.max(y[:])
    # y[:] = y[:] / maxy
    # meany = np.mean(y[:])
    # stdy = np.mean(y[:])
    # y[:] = (y[:] - meany) / stdy


feature_scaling()
# print(x)
w = np.array([0.] * cols)
# print(w)
# print(y)
# print(np.dot(x, w) + 200 - y)
# print(np.sum(np.dot(x, w) + 200 - y))
# print(x[:, 0])
# print(np.dot(np.sum(np.dot(x, w) + 200 - y), x[:, 0]))
# print(np.sum(np.dot(np.sum(np.dot(x, w) + 200 - y), x[:, 0])))

'''
Find partial derivative of cost function for w(j)
d/dw(j) = (1/m) * sigma((y_hat - y)^2 * x(j))
'''


def find_deriv_w(weights, bias, j):
    return np.dot(np.dot(x, weights) + bias - y, x[:, j]) / len(x)


'''
Find partial derivative of cost function for b
d/db = (1/m) * sigma((y_hat - y)^2)
'''


def find_deriv_b(weights, bias):
    return np.sum(np.dot(x, weights) + bias - y) / len(x)


'''
Perform gradient descent to minimize cost function
Simultaneously update w for all j and b by decreasing respective partial derivative * alpha from current value
'''


def gradient_descent(weights, bias, alpha, epoch):
    for i in range(epoch):
        temp = weights
        for j in range(cols):
            weights[j] = weights[j] - alpha * find_deriv_w(weights, bias, j)
        bias = bias - alpha * find_deriv_b(temp, bias)
        print("w: ", weights, "b: ", bias)
    return weights, bias


'''
Predict health insurance value using w and b
'''


def predict_value(features, weights, bias):
    return np.dot(features, weights) + bias


'''
Downscale relevant features in test data to 0 - 1 range
'''


def feature_scale_f(features):
    for i in range(0, cols):
        mx = np.max(x_copy[:, i])
        features[i] = features[i] / mx
    return features


weight, b = gradient_descent(w, min_bias, 3, 10000)
print("w: ", weight, "b: ", b)


'''
Ask for input features for testing
'''


while True:
    age = float(input("Age: "))
    sex = float(input("Sex (0/1): "))
    bmi = float(input("BMI: "))
    children = float(input("# Children: "))
    smoker = float(input("Smoker (0/1): "))
    region = float(input("Region (0/1/2/3 = SW/SE/NW/NE): "))

    f = np.array([age, sex, bmi, children, smoker, region])
    f = feature_scale_f(f)
    print(predict_value(f, weight, b))
