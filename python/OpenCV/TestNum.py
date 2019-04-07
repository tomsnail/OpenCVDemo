import numpy
import math
def softmax(isMatrix):
    m,n = numpy.shape(isMatrix)
    outMatrix = numpy.mat(numpy.zeros((m,n)))
    soft_sum = 0
    for idx in range(0,n):
        outMatrix[0,idx] = math.exp(isMatrix[0,idx])
        soft_sum += outMatrix[0,idx]
    for idx in range(0,n):
        outMatrix[0,idx] = outMatrix [0,idx] / soft_sum

    return outMatrix

def main():
    result = softmax(numpy.array([[1,2,1,2,1,1,3]]))
    print(result)


table = {'yangsong': 0, 'liuwei': 0, 'yangda': 0}
t = "yangsong"
table[t] = 1
print(table.get(t))
