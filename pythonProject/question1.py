import numpy as np
import tensorflow as tf

def loss_function(x):
    return 7*x**3 + 8*x**2 - 6*x
x=tf.variable(0,0)

optimizer = tf.keras.optimizers.SGD()

iteration = 100

for i in range(iteration):
    with tf.GradientTape() as tape:
        loss_value = loss_function(x)
    gradients = tape.gradient(loss_value, x.trainable_variables)
    optimizer.apply_gradients(zip(gradients, x.trainable_variables))

print("optimized value of x:",x.numpy())