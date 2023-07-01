## Introduction

The goal of this project is to use the Metropolis Hastings algorithm for Markov Chain Monte Carlo (MCMC) to decrypt an encoded
message. The message assumed to have an unknown deterministic function that, for each character in the message, maps to a corresponding
character within the same set, such that the output of that message when passed through the function looks like English. The message
has exactly 27 unique characters (26 lowercase letters and a space), so each function can be thought of as a permutation of these
characters. The output of the $i^{th}$ character through the function is then the value in the $i^{th}$ position of this permutation.

The intuition behind the suggested algorithm is that we can set up the problem up as a Markov chain whose steady state
distribution is that of the correct decryption function. This way, all we need to do is determine the steady state of the Markov
chain to know the target function.

## Intuition behind the MCMC algorithm

At a high level, we consider the following:

1. We are working in a state space of all possible functions (permutations).

2. Each function corresponds to a decoded message which may or may not look like English. The computer can know that it's
   more likely to be English if it shows more similarities with English when run against a certain metric called the plausibility
   score $p(\cdot)$, which in this case is the relative second-order frequencies of letters from English texts (that is, how likely any
   adjacent pair of letters is to exist in English, compared to every other pair in the message). Jane Austen's books are used as the
   reference texts.
  
4. Given any function $f$, we have two options for where to go next: we either stay at the current function we go to a new function $f^\*$
   suggested by an arbitrary stochastic matrix $\mathbf{Q}$. In this case, the matrix randomly suggests $f^\*$ to be the same as $f$,
   except that two characters in the permutation that $f$ corresponds to are switched at random.

5. We now have a choice on whether to accept or reject the $f^\*$. We do so by comparing the plausibility scores of $f^\*$ and $f$
   against each other. We accept $f^\*$ with probability $$\alpha = \min \left[ 1, \frac{p(f^\*)}{p(f)} \right]$$
   So if $f^\*$ is more similar to English than $f$, we are definitely accepting it since $p(f^\*)>p(f) \Rightarrow \alpha = 1$. If on the
   other hand $f$ is more similar to English than $f^*$, we *may* accept it, but we are less likely to do so for larger differences in
   similarity.

7. As a consequence, we drift towards functions with higher plausibility scores. The hope is that we have chosen a good metric
   that gives the target function (decoding to English itself) the highest plausibility score, or something close to the highest.
   Empirically, we see that it does.

The algorithm's implementation and output is in the python script MetropolisHastings.py, along with a sample text to decrypt.

**Note:** Since this is a stochastic algorithm, it does not always produce the desired output. Running it a few times should do the trick in that case.