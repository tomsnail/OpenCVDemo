import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

#修改代价函数为交叉熵
def mnist_op1():
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
    # loss = tf.reduce_mean(tf.square(y - prediction))
    #交叉熵
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=prediction))
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

#增加网络层次和节点，并使用dropout防止过拟合
def mnist_op2():
    #载入数据
    mnist = input_data.read_data_sets("./datas/mnist/",one_hot=True)

    #每个批次的大小
    batch_size = 100
    #计算一共有多少个批次
    n_batch = mnist.train.num_examples // batch_size
    print(n_batch)

    #定义两个
    x = tf.placeholder(tf.float32,[None,784])
    y = tf.placeholder(tf.float32,[None,10])
    #定义神经元dropout参数
    keep_prob = tf.placeholder(tf.float32)

    #创建神经网络

    W1 = tf.Variable(tf.truncated_normal([784,2000],stddev=0.1))
    b1 = tf.Variable(tf.zeros([2000])+0.1)
    L1 = tf.nn.tanh(tf.matmul(x,W1)+b1)
    L1_drop = tf.nn.dropout(L1,keep_prob)

    W2 = tf.Variable(tf.truncated_normal([2000, 2000], stddev=0.1))
    b2 = tf.Variable(tf.zeros([2000]) + 0.1)
    L2 = tf.nn.tanh(tf.matmul(L1_drop, W2) + b2)
    L2_drop = tf.nn.dropout(L2, keep_prob)

    W3 = tf.Variable(tf.truncated_normal([2000, 1000], stddev=0.1))
    b3 = tf.Variable(tf.zeros([1000]) + 0.1)
    L3 = tf.nn.tanh(tf.matmul(L2_drop, W3) + b3)
    L3_drop = tf.nn.dropout(L3, keep_prob)

    W4 = tf.Variable(tf.truncated_normal([1000, 10], stddev=0.1))
    b4 = tf.Variable(tf.zeros([10]) + 0.1)
    prediction = tf.nn.softmax(tf.matmul(L3_drop,W4)+b4)

    # 二次代价函数
    # loss = tf.reduce_mean(tf.square(y - prediction))
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=prediction))
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
        for epoch in range(31):
            print("start:",epoch)
            for batch in range(n_batch):
                print("start batch :", batch)
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.3})

            test_acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
            train_acc = sess.run(accuracy, feed_dict={x: mnist.train.images, y: mnist.train.labels, keep_prob: 1.0})
            print(epoch,test_acc,train_acc)

    pass

#修改优化器
def mnist_op3():
    #载入数据
    mnist = input_data.read_data_sets("./datas/mnist/",one_hot=True)

    #每个批次的大小
    batch_size = 100
    #计算一共有多少个批次
    n_batch = mnist.train.num_examples // batch_size
    print(n_batch)

    #定义两个
    x = tf.placeholder(tf.float32,[None,784])
    y = tf.placeholder(tf.float32,[None,10])
    #定义神经元dropout参数
    keep_prob = tf.placeholder(tf.float32)

    #创建神经网络

    W1 = tf.Variable(tf.truncated_normal([784,2000],stddev=0.1))
    b1 = tf.Variable(tf.zeros([2000])+0.1)
    L1 = tf.nn.tanh(tf.matmul(x,W1)+b1)
    L1_drop = tf.nn.dropout(L1,keep_prob)

    W2 = tf.Variable(tf.truncated_normal([2000, 2000], stddev=0.1))
    b2 = tf.Variable(tf.zeros([2000]) + 0.1)
    L2 = tf.nn.tanh(tf.matmul(L1_drop, W2) + b2)
    L2_drop = tf.nn.dropout(L2, keep_prob)

    W3 = tf.Variable(tf.truncated_normal([2000, 1000], stddev=0.1))
    b3 = tf.Variable(tf.zeros([1000]) + 0.1)
    L3 = tf.nn.tanh(tf.matmul(L2_drop, W3) + b3)
    L3_drop = tf.nn.dropout(L3, keep_prob)

    W4 = tf.Variable(tf.truncated_normal([1000, 10], stddev=0.1))
    b4 = tf.Variable(tf.zeros([10]) + 0.1)
    prediction = tf.nn.softmax(tf.matmul(L3_drop,W4)+b4)

    # 二次代价函数
    # loss = tf.reduce_mean(tf.square(y - prediction))
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=prediction))
    # 梯度下降训练函数

    # train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
    train_step = tf.train.AdamOptimizer(1e-2).minimize(loss)


    # 初始化变量
    init = tf.global_variables_initializer()

    #定义准确率
    correct_prediction = tf.equal(tf.argmax(y,1),tf.argmax(prediction,1))#argmax返回一维张量中最大值所在的位置
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))


    # 开始训练
    with tf.Session() as sess:
        sess.run(init)
        for epoch in range(31):
            print("start:",epoch)
            for batch in range(n_batch):
                print("start batch :", batch)
                batch_xs,batch_ys = mnist.train.next_batch(batch_size)
                sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.3})

            test_acc = sess.run(accuracy,feed_dict={x:mnist.test.images,y:mnist.test.labels,keep_prob:1.0})
            train_acc = sess.run(accuracy, feed_dict={x: mnist.train.images, y: mnist.train.labels, keep_prob: 1.0})
            print(epoch,test_acc,train_acc)

    pass

if __name__ == '__main__':
    mnist_op3()