import tensorflow as tf
import numpy as np
#生成100个随机点
x_data = np.random.rand(100)
y_data = x_data*0.3+0.2 #每个点满足y=x*0.3+0.2这个线性函数

#定义线性模型
b = tf.Variable(0.)
k = tf.Variable(0.)
y = k*x_data+b
#定义损失函数
loss = tf.reduce_mean(tf.square(y_data-y))
#梯度下降训练函数
optimizer = tf.train.GradientDescentOptimizer(0.2)
#最小化代价函数
train = optimizer.minimize(loss)
#初始化变量
init = tf.global_variables_initializer()
#开始训练
with tf.Session() as sess:
    sess.run(init)
    for step in range(201):
        sess.run(train)
        if step % 20 == 0:
            print(step,sess.run(loss),sess.run([k,b]))

