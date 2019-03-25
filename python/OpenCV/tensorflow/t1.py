import tensorflow as tf
import numpy as np

def test_tf_1():
    inputX = np.random.rand(100)
    inputY = np.multiply(3,inputX)+1
    x = tf.placeholder("float32")
    weight = tf.Variable(0.25)
    bias = tf.Variable(0.25)
    y = tf.multiply(weight,x)+bias
    y_ = tf.placeholder("float32")
    loss = tf.reduce_sum(tf.pow((y-y_),2))
    train_step = tf.train.GradientDescentOptimizer(0.001).minimize(loss)
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    for _ in range(100000):
        sess.run(train_step,feed_dict={x:inputX,y_:inputY})
        if _%20 == 0:
            _w = weight.eval(session=sess)
            _b = bias.eval(session=sess)
            print("W value ：",_w," bias value :",_b)
            inputX = _w
            inputY = _b

def hello_tensorflow():
    inputX = np.random.rand(3000,1)
    noise = np.random.normal(0,0.05,inputX.shape)
    outputY = inputX*4+1+noise

    weight1 = tf.Variable(np.random.rand(inputX.shape[1],4))
    bias1 = tf.Variable(np.random.rand(inputX.shape[1],4))
    x1 = tf.placeholder(tf.float64,[None,1])
    y1_ = tf.matmul(x1,weight1)+bias1

    y = tf.placeholder(tf.float64,[None,1])
    loss = tf.reduce_mean(tf.reduce_sum(tf.square((y1_-y)),reduction_indices=[1]))
    train = tf.train.GradientDescentOptimizer(0.25).minimize(loss)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    for i in range(1000):
        sess.run(train,feed_dict={x1:inputX,y:outputY})

    print(weight1.eval(sess))
    print("-----------------")
    print(bias1.eval(sess))
    print("-----------------------")

    x_data = np.matrix([[1.],[2.],[3.]])
    print(sess.run(y1_,feed_dict={x1:x_data}))
    pass

def hello_tensorflow2():
    inputX = np.random.rand(3000,1)
    noise = np.random.normal(0,0.05,inputX.shape)
    outputY = inputX*4+1+noise

    weight1 = tf.Variable(np.random.rand(inputX.shape[1],4))
    bias1 = tf.Variable(np.random.rand(inputX.shape[1],4))
    x1 = tf.placeholder(tf.float64,[None,1])
    y1_ = tf.matmul(x1,weight1)+bias1

    weight2 = tf.Variable(np.random.rand(4, 1))
    bias2 = tf.Variable(np.random.rand(inputX.shape[1], 1))
    y2_ = tf.matmul(y1_, weight2) + bias2

    y = tf.placeholder(tf.float64,[None,1])
    loss = tf.reduce_mean(tf.reduce_sum(tf.square((y2_-y)),reduction_indices=[1]))
    train = tf.train.GradientDescentOptimizer(0.25).minimize(loss)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    for i in range(1000):
        sess.run(train,feed_dict={x1:inputX,y:outputY})

    print(weight1.eval(sess))
    print("-----------------")
    print(bias1.eval(sess))
    print("-----------------------")

    print(weight2.eval(sess))
    print("-----------------")
    print(bias2.eval(sess))
    print("-----------------------")

    x_data = np.matrix([[1.],[2.],[3.]])
    print(sess.run(y2_,feed_dict={x1:x_data}))
    pass



def main():
    #test_tf_1()
    #hello_tensorflow()
    hello_tensorflow2()
    pass

main()