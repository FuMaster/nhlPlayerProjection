import tensorflow as tf
import numpy as np
import input_data_c

def init_weights(shape):
    return tf.Variable(tf.random_normal(shape, stddev=0.01))

def model(X, w_h, w_o):
    h = tf.nn.sigmoid(tf.matmul(X, w_h)) # this is a basic mlp, think 2 stacked logistic regressions
    return tf.matmul(h, w_o) # note that we dont take the softmax at the end because our cost fn does that for us

def model2(X, w_h, w_h2, w_o, p_drop_input, p_drop_hidden): # this network is the same as the previous one except with an extra hidden layer + dropout
    X = tf.nn.dropout(X, p_drop_input)
    h = tf.nn.relu(tf.matmul(X, w_h))

    h = tf.nn.dropout(h, p_drop_hidden)
    h2 = tf.nn.relu(tf.matmul(h, w_h2))

    h2 = tf.nn.dropout(h2, p_drop_hidden)

    return tf.matmul(h2, w_o)

def float_arr(arr):
	return map(float,arr)

data_sets = input_data_c.read_data_sets()
trX, trY, teX, teY = map(float_arr,data_sets.train.stats), map(float_arr,data_sets.train.labels), \
					map(float_arr,data_sets.test.stats), map(float_arr,data_sets.test.labels)

X = tf.placeholder("float", [None, 34])
Y = tf.placeholder("float", [None, 9])

n=480		
w_h = init_weights([34, n]) # create symbolic variables
w_h2 = init_weights([n,n])
w_o = init_weights([n, 9])
p_keep_input = tf.placeholder('float')
p_keep_hidden = tf.placeholder('float')

#py_x = model(X, w_h, w_o)
py_x = model2(X, w_h, w_h2, w_o, p_keep_input, p_keep_hidden)

cross_entropy = -tf.reduce_sum(Y*tf.log(py_x))
mean_squared_error = tf.reduce_mean(tf.square(Y-py_x))

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(py_x, Y)) # compute costs
#0.1, 0.01, 0.25
train_op = tf.train.GradientDescentOptimizer(0.25).minimize(mean_squared_error) # construct an optimizer
predict_op = py_x#tf.argmax(py_x, 1)

sess = tf.Session()
init = tf.initialize_all_variables()
sess.run(init)

#no hidden layer
for i in range(1000):
    #for start, end in zip(range(0, len(trX), 128), range(128, len(trX), 128)):
    sess.run(train_op, feed_dict={X: trX, Y: trY, p_keep_hidden: 0.5, p_keep_input: 0.8})
    #print i, teY[0], sess.run(predict_op, feed_dict={X: teX, Y: teY})[0]
    print i, np.mean(np.mean(teY - sess.run(predict_op, feed_dict={X: teX, Y:teY, p_keep_hidden: 1.0, p_keep_input: 1.0}),axis=1))
    #tmp.append(np.mean(np.mean(np.square(teY - sess.run(predict_op, feed_dict={X: teX, Y:teY})),axis=1)))
#ret.append(tmp)


