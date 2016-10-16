# IPython log file

get_ipython().magic(u'paste')
import tensorflow as tf
sess = tf.InteractiveSession()
get_ipython().magic(u'save file_name.py')
get_ipython().run_cell_magic(u'writefile', u'filename.py', u'')
get_ipython().magic(u'save')
get_ipython().magic(u'save filename.py')
get_ipython().magic(u'save filename.py _')
get_ipython().magic(u'history -f /tmp/history.py')
hi
get_ipython().magic(u'history -f /tmp/history.py')
a=b
a=2
get_ipython().magic(u'history -f /tmp/history.py')
a=2
get_ipython().magic(u'history /tmp/history.py')
a=2
get_ipython().magic(u'logstart')
import tensorflow as tf
sess = tf.InteractiveSession()
input_size = 11
input = tf.placeholder(tf.float32, shape=[None,11])
score = tf.placeholder(tf.float32,shape=[None,1])
w1 = tf.Variable(tf.random_uniform([11,50]))
b1 = tf.Variable(tf.random_uniform([50]))
op1 = tf.sigmoid(tf.matmul(input,w1)+b1)
w2 = tf.Variable(tf.random_uniform([50,2]))
b2 = tf.Variable(tf.random_uniform([2]))
op2 = tf.sigmoid(tf.matmul(op1,w2)+b2)
w3 = tf.Variable(tf.random_uniform([2,1]))
b3 = tf.Variable(tf.random_uniform([1]))
pred = tf.sigmoid(tf.matmul(op2,w3)+b3)
optimizer = tf.train.GradientDescentOptimizer(0.01)
loss_m = tf.reduce_sum(pred-score)
train_step = optimizer.minimize(loss_m)
