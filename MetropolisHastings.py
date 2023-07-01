import numpy
import random
import copy
from scipy.stats import uniform

def MCMC(code: str, reference: str) -> str:

    code_array = [char for char in code]

    def char2num(c): return 26 if c == ' ' else ord(c) - ord('a')
    def num2char(n): return ' ' if n == 26 else chr(n + ord('a'))
    code_nums = [char2num(c) for c in code_array]

    with open(reference, "r") as M_file:
        M_string = [line.strip().split('\t') for line in M_file]
    M = [[int(n) + 1 for n in row] for row in M_string] # shifted by 1

    def switch_randomly(f):
        a = random.randint(0, len(f)-1)
        b = random.randint(0, len(f)-1)
        f_star = copy.deepcopy(f)
        f_star[a] = f[b]
        f_star[b] = f[a]
        return f_star

    def apply(f): return [f[i] for i in code_nums]

    def alpha(f, f_star):
        f_star_array = apply(f_star)
        f_array = apply(f)
        M_f_star = [numpy.log(M[i][f_star_array[ind+1]]) for ind, i in enumerate(f_star_array) if ind < len(f_star_array)-1]
        M_f = [numpy.log(M[i][f_array[ind+1]]) for ind, i in enumerate(f_array) if ind < len(f_array)-1]
        return numpy.exp(min(sum(M_f_star) - sum(M_f), 0))

    def accept(alpha): return uniform.rvs(loc=0, scale=1) < alpha
    def decrypt(f): return "".join([num2char(n) for n in apply(f)])

    iterations = [100, 200, 500, 1000, 2000, 3000, 4000, 5000]
    f = [i for i in range(27)]
    decrypted = ""
    for i in range(5000):
        f_star = switch_randomly(f)
        if accept(alpha(f, f_star)): f = f_star
        for ind, j in enumerate(iterations):
            if i == j-1: print(decrypt(f) + "\n")
            if ind == len(iterations)-1: decrypted = decrypt(f)

    return decrypted


if __name__ == '__main__':

    with open("Code.txt", "r") as encrypted:
        code = [line for line in encrypted]

    decrypted = MCMC(code[0], "AustenCount.txt")