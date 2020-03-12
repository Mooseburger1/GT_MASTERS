import tensorflow as tf
from collections import deque
import numpy as np
import random



DISCOUNT = 0.99
REPLAY_MEMORY_SIZE = 20_000  # How many last steps to keep for model training
MIN_REPLAY_MEMORY_SIZE = 1_000  # Minimum number of steps in a memory to start training
MINIBATCH_SIZE = 128  # How many steps (samples) to use for training
UPDATE_TARGET_EVERY = 10  # Terminal states (end of episodes)


MEMORY_FRACTION = 0.20





#  Stats settings
SHOW_PREVIEW = False

class DQNAgent:
    def __init__(self):

        # Main model
        self.model = self.create_model()

        # Target network
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        # An array with last n steps for training
        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)


        # Used to count when to update target network with main network's weights
        self.target_update_counter = 0

        #Loss function
        self.train_mse_loss_fn = tf.keras.losses.MSE

        #optimizer
        self.optimizer = tf.keras.optimizers.Adam(0.001, beta_1=0.5)

        self.checkpoint = tf.train.Checkpoint(optimizer = self.optimizer, model = self.model)

        self.episode = None

        

    def create_model(self):
        
        initializer = tf.random_normal_initializer(0., 0.02)
        inputs = tf.keras.layers.Input(shape=[1,8])

        x = inputs

        x = tf.keras.layers.Dense(units=256, use_bias=True, kernel_initializer=initializer, bias_initializer=initializer)(x)
        x = tf.keras.layers.ReLU()(x)
        x = tf.keras.layers.Dense(256, use_bias=True, activation = 'sigmoid', kernel_initializer=initializer, bias_initializer=initializer)(x)
        x = tf.keras.layers.Dense(4, use_bias=True, kernel_initializer=initializer, bias_initializer=initializer)(x)

        model = tf.keras.Model(inputs=inputs, outputs=x)
        return model

    @tf.function
    def train_step(self, X, y):
        with tf.GradientTape() as tape:
            forward = self.model(X, training=True)

            loss = self.train_mse_loss_fn(y, forward)

            grads = tape.gradient(loss, self.model.trainable_variables)

            self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    @tf.function
    def fit(self, X, y, epochs):

        for _ in range(epochs):
            
            self.train_step(X,y)

        

        

    # Adds step's data to a memory replay array
    # (observation space, action, reward, new observation space, done)
    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    # Trains main network every step during episode
    def train(self, terminal_state, step):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < MIN_REPLAY_MEMORY_SIZE:
            return

        # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = tf.reshape(np.array([transition[0] for transition in minibatch]), [MINIBATCH_SIZE, -1, 8])
        current_qs_list = self.model(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = tf.reshape(np.array([transition[3] for transition in minibatch]), [MINIBATCH_SIZE, -1, 8])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (current_state, action, reward, _, done) in enumerate(minibatch):

            # If not a terminal state, get new q from future states, otherwise set it to 0
            # almost like with Q Learning, but we use just part of equation here
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_qs = current_qs_list[index]

            current_qs.numpy()[0][action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        # Fit on all samples as one batch, log only on terminal state
        self.fit(X = tf.reshape(np.array(X), [-1, 1, 8]), y = tf.reshape(np.array(y), [-1, 1, 4]), epochs = 100)
        if self.episode % 10 == 0:
            self.checkpoint.save(file_prefix='models/ckpt_{}'.format(int(self.episode / 10)))
        # Update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    # Queries main network for Q values given current observation space (environment state)
    def get_qs(self, state):
        return self.model(tf.reshape(np.array(state), [-1, 1, 8]))[0]