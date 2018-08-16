
import matplotlib.pyplot as plt
import numpy as np 

def sigmoid(x):
    return 1/(1+np.exp(-x))
def tanh(x):
    return (np.exp(x) - np.exp(-x))/(np.exp(x) + np.exp(-x))

relu = lambda x: max(0,x)
lrelu = lambda x: x if x >= 0 else 0.3*x
elu = lambda x: x if x >= 0 else 1.0*(np.exp(x)-1)

x = np.arange(-10, 10)
sigmoid_v = np.vectorize(sigmoid)
tanh_v = np.vectorize(tanh)
relu_v = np.vectorize(relu)
lrelu_v = np.vectorize(lrelu)
elu_v = np.vectorize(elu)

functions = [{"title": "Sigmoid", "function": sigmoid_v},
             {"title": "Tanh", "function": tanh_v},
             {"title": "Relu", "function": relu_v},
             {"title": "Leaky_Relu", "function": lrelu_v},
             {"title": "ELU", "function": elu_v}
            ]
for function in functions:
    plt.style.use("ggplot")
    plt.figure()
    plt.title(function["title"])
    plt.plot(x, function["function"](x), color="blue")
    plt.savefig("../images/"+function["title"] +".png")

