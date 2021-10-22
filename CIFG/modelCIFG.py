import numpy as np

class LSTM:
    def __init__(self, char_to_idx, idx_to_char, vocab_size, n_h=100, seq_len=25,
                 epochs=2, lr=0.001, beta1=0.9, beta2=0.999):
        """
        Implementation of simple character-level LSTM using Numpy
        """
        self.char_to_idx = char_to_idx  # characters to indices mapping
        self.idx_to_char = idx_to_char  # indices to characters mapping
        self.vocab_size = vocab_size  # no. of unique characters in the training data
        self.n_h = n_h  # no. of units in the hidden layer
        self.seq_len = seq_len  # no. of time steps, also size of mini batch
        self.epochs = epochs  # training iterations
        self.eps = 1e-12

        # Optimization Parameters
        self.lr = lr  # learning rate
        self.beta1 = beta1  # 1st momentum parameter
        self.beta2 = beta2  # 2nd momentum parameter

        # -----initialise weights and biases-----#
        self.params = {}
        std = (1.0 / np.sqrt(self.vocab_size + self.n_h))  # Randomized Xavier GLOROT initialisation
        # I slightly varied the standard Glorot initialization, as it seemed to do better in some of my tests while checking for other datasets too. 

        # forget gate
        self.params["Wf"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bf"] = np.zeros((self.n_h, 1))

        # input gate
        self.params["Wi"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bi"] = np.zeros((self.n_h, 1))

        # cell gate
        self.params["Wc"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std 
        self.params["bc"] = np.zeros((self.n_h, 1))

        # output gate
        self.params["Wo"] = np.random.randn(self.n_h, self.n_h + self.vocab_size) * std
        self.params["bo"] = np.zeros((self.n_h, 1))

        # output
        self.params["Wv"] = np.random.randn(self.vocab_size, self.n_h) * \
                            (1.0 / np.sqrt(self.vocab_size))
        self.params["bv"] = np.zeros((self.vocab_size, 1))

        # -----initialise gradients and Adam parameters-----#
        self.grads = {}
        self.adam_params = {}

        for key in self.params:
            self.grads["d" + key] = np.zeros_like(self.params[key])
            self.adam_params["m" + key] = np.zeros_like(self.params[key])
            self.adam_params["v" + key] = np.zeros_like(self.params[key])

        self.smooth_loss = -np.log(1.0 / self.vocab_size) * self.seq_len
        self.perp = np.exp(self.smooth_loss)
        return


    def sigmoid(self, x, grad=False):
        sigm = 1/(1+np.exp(-x))
        if grad:
            return sigm * (1 - sigm)
        return sigm

    def tanh(self, x, grad=False):
        if grad:
            dt=1-(np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))**2
            return dt
        return (np.exp(x)-np.exp(-x))/(np.exp(x)+np.exp(-x))

    # Generic Softmax with numerical stability
    def softmax(self, x):
        return np.exp(x - np.max(x)) / np.sum(np.exp(x - np.max(x)))

    def dsigmoid(self, y):
        return y * (1 - y)

    def dtanh(self, y):
        return 1 - y * y

    def clip_grads(self):
        """
        Helps with exploding gradients
        """
        for key in self.grads:
            np.clip(self.grads[key], -2, 2, out=self.grads[key])
        return

    def reset_grads(self):
        """
        Resets grads to zero before each backprop step ; This is equivalent to torch.zero_grad() to avoid hyperstepping during convex optimization
        """
        # This is equivalent to torch.zero_grad() to avoid hyperstepping during convex optimization
        for key in self.grads:
            self.grads[key].fill(0)
        return

    def update_params(self, batch_num):
        """
        ADAM Optimizer (As it performs better than SGD)
        # ref - https://towardsdatascience.com/how-to-implement-an-adam-optimizer-from-scratch-76e7b217f1cc
        """
        for key in self.params:
            # Momentum Calculation
            self.adam_params["m" + key] = self.adam_params["m" + key] * self.beta1 + \
                                          (1 - self.beta1) * self.grads["d" + key]

            ## rms beta 2
            self.adam_params["v" + key] = self.adam_params["v" + key] * self.beta2 + \
                                          (1 - self.beta2) * self.grads["d" + key] ** 2

            # Bias Correlation
            correctedBias1 = (1 - self.beta1 ** batch_num)
            correctedBias2 = (1 - self.beta2 ** batch_num)
            m_correlated = self.adam_params["m" + key] / correctedBias1
            v_correlated = self.adam_params["v" + key] / correctedBias2
            self.params[key] = self.params[key] - self.lr * m_correlated / (np.sqrt(v_correlated) + self.eps)
        return

    def sample(self, h_prev, c_prev, sample_size):
        """
        Outputs a sample sequence from the model
        """
        x = np.zeros((self.vocab_size, 1))
        h,c = h_prev, c_prev
        sample_string = ""

        for _ in range(sample_size):
            y_hat, _, h, _, c, _, _, _, _ = self.forward_step(x, h, c)

            # random index within the prob dist of y_hat.ravel()
            #y_hat = np.asarray(y_hat).astype('float64')
            idx = np.random.choice(range(self.vocab_size), p=y_hat.ravel())
            x = np.zeros((self.vocab_size, 1))
            x[idx] = 1

            char = self.idx_to_char[idx]
            sample_string += char
        return sample_string

    def forward_step(self, x, h_prev, c_prev):
        """
        Implements the forward propagation for one time step
        """
        # Concatenate the h from previous timestep and x from current time step
        z = np.row_stack((h_prev, x))

        # Input is the only gate we calculate here. The definition for input gate was provided in the README.md file.
        i = self.sigmoid(np.dot(self.params["Wi"], z) + self.params["bi"])

        # of course, since this is CIFG, the forget gate needs to assert to the same shape as input but a 1 - i in a vectorized format
        f = np.ones(i.shape) - i
        c_bar = self.tanh(np.dot(self.params["Wc"], z) + self.params["bc"])

        c = f * c_prev + i * c_bar
        o = self.sigmoid(np.dot(self.params["Wo"], z) + self.params["bo"])
        h = o * self.tanh(c)

        # The below cell is the logists
        v = np.dot(self.params["Wv"], h) + self.params["bv"]

        # Numerically stable softmax
        y_hat = self.softmax(v)
        return y_hat, v, h, o, c, c_bar, i, f, z

    def backward_step(self, y, y_hat, dh_next, dc_next, c_prev, z, f, i, c_bar, c, o, h):
        """
        Implements the backward propagation for one time step
        """
        dv = np.copy(y_hat)
        dv[y] -= 1

        self.grads["dWv"] += np.dot(dv, h.T)
        self.grads["dbv"] += dv

        dh = np.dot(self.params["Wv"].T, dv)
        dh += dh_next

        do = dh * self.tanh(c)
        da_o = do * self.dsigmoid(o)
        self.grads["dWo"] += np.dot(da_o, z.T)
        self.grads["dbo"] += da_o

        dc = dh * o * (1 - self.tanh(c) ** 2)
        dc += dc_next

        dc_bar = dc * i
        da_c = dc_bar * (1 - c_bar ** 2)
        self.grads["dWc"] += np.dot(da_c, z.T)
        self.grads["dbc"] += da_c

        di = dc * c_bar
        da_i = di * self.dsigmoid(i)
        self.grads["dWi"] += np.dot(da_i, z.T)
        self.grads["dbi"] += da_i

        df = dc * c_prev
        # f here is the `tricked` value for CIFG
        da_f = df * self.dsigmoid(f)
        self.grads["dWf"] += np.dot(da_f, z.T)
        self.grads["dbf"] += da_f

        # Note that even though this is a CIFG Implementation, we DO NOT skip the dwi and dfi, as the forget input is already 1 - i, so the grad would give us the correct differential.
        dz = (np.dot(self.params["Wf"].T, da_f)
              + np.dot(self.params["Wi"].T, da_i)
              + np.dot(self.params["Wc"].T, da_c)
              + np.dot(self.params["Wo"].T, da_o))

        dh_prev = dz[:self.n_h, :]
        dc_prev = f * dc
        return dh_prev, dc_prev

    def forward_backward(self, x_batch, y_batch, h_prev, c_prev):
        """
        The forward and backward propagation for one mini batch
        """
        x, z = {}, {}
        f, i, c_bar, c, o = {}, {}, {}, {}, {}
        y_hat, v, h = {}, {}, {}

        # Values at t= - 1
        h[-1] = h_prev
        c[-1] = c_prev

        loss = 0
        for t in range(self.seq_len):
            x[t] = np.zeros((self.vocab_size, 1))
            x[t][x_batch[t]] = 1

            y_hat[t], v[t], h[t], o[t], c[t], c_bar[t], i[t], f[t], z[t] = \
                self.forward_step(x[t], h[t - 1], c[t - 1])

            loss += -np.log(y_hat[t][y_batch[t], 0])

        self.reset_grads()

        dh_next = np.zeros_like(h[0])
        dc_next = np.zeros_like(c[0])

        for t in reversed(range(self.seq_len)):
            dh_next, dc_next = self.backward_step(y_batch[t], y_hat[t], dh_next,
                                                  dc_next, c[t - 1], z[t], f[t], i[t],
                                                  c_bar[t], c[t], o[t], h[t])
        return loss, h[self.seq_len - 1], c[self.seq_len - 1]

    def train(self, X, verbose=True):
        """
        Main method of the LSTM class where training takes place
        """
        J = []  # to store losses
        PP = [] # to store perplexity

        # Proper division here
        num_batches = len(X) // self.seq_len
        X_trimmed = X[: num_batches * self.seq_len]

        for epoch in range(self.epochs):
            h_prev = np.zeros((self.n_h, 1))
            c_prev = np.zeros((self.n_h, 1))

            for j in range(0, len(X_trimmed) - self.seq_len, self.seq_len):
                # prepare batches
                x_batch = [self.char_to_idx[ch] for ch in X_trimmed[j: j + self.seq_len]]
                y_batch = [self.char_to_idx[ch] for ch in X_trimmed[j + 1: j + self.seq_len + 1]]

                loss, h_prev, c_prev = self.forward_backward(x_batch, y_batch, h_prev, c_prev)

                # smooth out loss and store in list
                self.smooth_loss = self.smooth_loss * 0.999 + loss * 0.001
                self.perp = np.exp(self.smooth_loss)

                # Append to final lists
                J.append(self.smooth_loss)
                PP.append(self.perp)

                self.clip_grads()

                batch_num = epoch * self.epochs + j / self.seq_len + 1
                self.update_params(batch_num)
                
                # print out loss and sample string
                if verbose:
                    if j % 400000 == 0:
                        print('Epoch:', epoch, '\tBatch:', j, "-", j + self.seq_len,
                              '\tLoss:', round(self.smooth_loss, 2))
                        print('Perplexity: ', self.perp)
                        print("\n")
                        s = self.sample(h_prev, c_prev, sample_size=250)
                        print(s, "\n")

        return J, PP, self.params
