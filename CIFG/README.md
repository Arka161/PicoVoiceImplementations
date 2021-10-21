# CIFG Implementation 

CIFG is basically a variation of RNN (LSTM), and the only difference is that the input gate and the forget gate are coupled together. 

## General LSTM Theory

The Forget Gate is responsible for deciding what information should be removed from the cell state. It is _normally_ a sigmoid of input x_t at time t, and it having a sum with h_t, which is multiplied by the weights, and there is an addition with the bias. 

However, in this case, the numpy array looks like (from a 10,000 feet overview):

```
forget = 1 - input
```

Forget formulation:  

```
f_t = sigmoid(x_t * u_f + h_(t-1) * w_f + b_f)
```

x_t has the size batch x feature vector. 

u_f has the size of feature vector x hidden units. 

h_(t-1) has the size batch size x hidden units. 

w_f has the size hidden units x hidden units 

bias (b_f) has a size of batch x hidden units. 


If the forget responds with 0, cell state is removed. Else, it's retained. 

Input Gate: 

It is responsible for deciding what information should be _stored_ in the cell state (as opposed to remove).

Let us look at the formulation. 
```
i_t = sigmoid(x_f * u_i + h_(t-1) * w_i + b_i) 
```

0 -> Information will not be stored. 

1 -> Information will be stored/updated. 

Input state is combined with Candidate State. It is represented by the tan hyperbolic function, and it holds the new information. It is controlled by the input gate. 


Output Gate: 

A lot of information is in the cell state (memory). The output gate decides what input should be taken from the cell state to give as final output.

``` 
o_t = sigmoid(x_f * u_o + h_(f-1) * w_o + b_0) 
```

Finally, a forward propagation yields the required output. 




