import math

# Given data
c_w1_wn = 17  # Frequency of "t. i." together
c_w1 = 19     # Frequency of "t."
c_w2 = 17     # Frequency of "i."
N = 267097    # Total number of words in the corpus
n = 2         # Length of the n-gram (bigram in this case)

# Calculate expected frequency E(w1...wn)
E_w1_wn = (c_w1 * c_w2) / (N ** (n - 1))

# Mutual Information (MI)
MI = math.log2(c_w1_wn / E_w1_wn)

# MI^3
MI3 = math.log2((c_w1_wn ** 3) / E_w1_wn)

# Dice coefficient
Dice = (n * c_w1_wn) / (c_w1 + c_w2)

# Log-Dice
logDice = 14 + math.log2(Dice)

# t-test
t_score = (c_w1_wn - E_w1_wn) / math.sqrt(c_w1_wn)

# Log-Likelihood (LL)
LL = 2 * (c_w1_wn * math.log10(c_w1_wn / E_w1_wn) - (c_w1_wn - E_w1_wn))

# Output the results
print(f"MI: {MI}")
print(f"MI3: {MI3}")
print(f"Dice: {Dice}")
print(f"logDice: {logDice}")
print(f"t-score: {t_score}")
print(f"simple-LL: {LL}")