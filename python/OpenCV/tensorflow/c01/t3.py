import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

def job_1():
    #生成200个随机点
    x_data = np.linspace(-0.5,0.5,200)[:,np.newaxis]
    noise = np.random.normal(0,0.2,x_data.shape)
    y_data = np.square(x_data)+noise

    #定义两个placeholder
    x = tf.placeholder(tf.float32,[None,1])
    y = tf.placeholder(tf.float32, [None, 1])

    #定义神经网络中间层

    Weights_L1 = tf.Variable(tf.random_normal([1,10]))
    biases_L1 = tf.Variable(tf.zeros([1,10]))
    Wx_plus_L1 = tf.matmul(x,Weights_L1)+biases_L1
    L1 = tf.nn.tanh(Wx_plus_L1)

    #定义输出层
    Weights_L2 = tf.Variable(tf.random_normal([10,1]))
    biases_L2 = tf.Variable(tf.zeros([1, 1]))
    Wx_plus_L2 = tf.matmul(L1, Weights_L2) + biases_L2
    prediction = tf.nn.tanh(Wx_plus_L2)

    #二次代价函数
    loss = tf.reduce_mean(tf.square(y-prediction))

    # 梯度下降训练函数
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
    # 初始化变量
    init = tf.global_variables_initializer()
    # 开始训练
    with tf.Session() as sess:
        sess.run(init)
        for i in range(2000):
            sess.run(train_step,feed_dict={x:x_data,y:y_data})

        prediction_value = sess.run(prediction,feed_dict={x:x_data})

        plt.figure()
        plt.scatter(x_data,y_data)
        plt.plot(x_data,prediction_value,'r-',lw=5)
        plt.show()

    pass

def mnist():
    #载入数据
    mnist = input_data.read_data_sets("./datas/mnist/",one_hot=True)

    #每个批次的大小
    batch_size = 100
    #计算一共有多少个批次
    n_batch = mnist.train.num_examples // batch_size

    #定义两个
    x = tf.placeholder(tf.float32,[None,784])
    y = tf.placeholder(tf.float32,[None,10])

    #创建神经网络
    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))
    prediction = tf.nn.softmax(tf.matmul(x,W)+b)

    # 二次代价函数
    loss = tf.reduce_mean(tf.square(y - prediction))

    # 梯度下降训练函数
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
    # 初始化变量
    init = tf.global_variables_initializer()

    #定义准确率
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))#argmax返回一维张量中最大值所在的位置
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


    # 开始训练
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(21):
            for batch in range(n_batch):
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys})

            acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
            print(epoch,acc)

    pass

def mnist_op():
    #载入数据
    mnist = input_data.read_data_sets("./datas/mnist/",one_hot=True)

    #每个批次的大小
    batch_size = 50
    #计算一共有多少个批次
    n_batch = mnist.train.num_examples // batch_size

    #定义两个
    x = tf.placeholder(tf.float32,[None,784])
    y = tf.placeholder(tf.float32,[None,10])

    #创建神经网络

    Weights_L1 = tf.Variable(tf.zeros([784,10]))
    biases_L1 = tf.Variable(tf.zeros([10]))
    Wx_plus_L1 = tf.matmul(x, Weights_L1) + biases_L1
    L1 = tf.nn.tanh(Wx_plus_L1)

    W = tf.Variable(tf.zeros([784,10]))
    b = tf.Variable(tf.zeros([10]))
    prediction = tf.nn.softmax(tf.matmul(Wx_plus_L1,W)+b)

    # 二次代价函数
    loss = tf.reduce_mean(tf.square(y - prediction))

    # 梯度下降训练函数
    train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
    # 初始化变量
    init = tf.global_variables_initializer()

    #定义准确率
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))#argmax返回一维张量中最大值所在的位置
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


    # 开始训练
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(100):
            for batch in range(n_batch):
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys})

            acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels})
            print(epoch,acc)

    pass




if __name__ == '__main__':
    # job_1()
    mnist_op()