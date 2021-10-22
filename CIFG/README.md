# CIFG Implementation 

General LSTM theory is availabe in the `THEORY.md` file in this same folder. 

First, here's an execellent explanation from Colah's blog post: 

![image](https://user-images.githubusercontent.com/20723780/138414303-0aa599bf-3e31-40c3-8e30-6a5e9e392415.png)

We basically implement this in a vanilla LSTM RNN-esque architecture. 

## Design decisions:

1. For optimization, we used a standard ADAM optimizer, which works on the intuition on RMS prop + two beta values. 
2. Weights have been initialized using the Xavier GLOROT scheme. I tried random weights too, but the loss didn't decrease. So only GLOROT worked. 
3. Cross Entropy Loss is used, and perplexity is used just as a metric (not for ADAM optimization).
4. We reset the gradients before each backpropagation step (akin to `torch.zero_grad()`). 
5. In forward, we set the forget gate as `f = np.ones(i.shape) - i`.
6. Gradients are clipped to avoid exploding gradient issues that can incur very large updates to neural network weights. 

## Evaluation: 

We use a regular cross entropy loss, and a perplexity metric. 

![image](https://user-images.githubusercontent.com/20723780/138415573-64ad2e7c-b1f0-44d1-8628-4f099e4aba4c.png)

The cross entropy loss _maximizes_ the probability of the given next true word, and in theory, perplexity is implemented as the exponential of the cross entropy loss. Perplexity in this scenario can be easy to understand from a _human_ perspective, as whenever we try to predict the next words, we have a choice between *n* words, where *n* denotes the perplexity. 

Furthermore, the cross entropy is a very textbook loss for problems/formulations such as these. We use it over regression based losses like the squared error loss as we want to perform Convex optimization, that enables us to efficiently train a deep network. The slide below from Grosse et. al talks about the intuition nicely. 

![image](https://user-images.githubusercontent.com/20723780/138416248-eddf6e62-eeef-4ccb-8b96-013c42ada084.png)

## Sample text generated after a few epochs: 

 ```
  ill me tain in sault
  i puan,
  and mirn a gended agioly.
  resban nath as for alon ade id,
  whereit truths to any eyes thee:
  and with thit the mise tote mechiend:
  but lefs my love, hath my love, to others my sifher laim man, and to knived hath boly
 ```
 
 ## Usage:
 
 ```
 conda install -c conda-forge jupyterlab
 jupyter-lab
 #open driverNotebook.ipynb
 ```
 
 NOTE: Since Numpy does not support GPU, we have the training done on the CPU. It might be a little slow if your text file is too large. 

### Reference: 

1. https://blog.varunajayasiri.com/numpy_lstm.html
2. https://colah.github.io/posts/2015-08-Understanding-LSTMs/
3. https://en.wikipedia.org/wiki/Long_short-term_memory#:~:text=Long%20short%2Dterm%20memory%20(LSTM)%20is%20an%20artificial%20recurrent,the%20field%20of%20deep%20learning.&text=LSTM%20networks%20are%20well%2Dsuited,events%20in%20a%20time%20series.
4. https://towardsdatascience.com/perplexity-in-language-models-87a196019a94
