import math

# Given values
a = 17
b = 0.000000000000000001
c = 267097
d = 400391

# Calculate E1 and E2
total = c + d
E1 = c * (a + b) / total
E2 = d * (a + b) / total

# Calculate LL, BIC, log ratio, OR, %DIFF
LL = 2 * ((a * math.log(a / E1)) + (b * math.log(b / E2)))
BIC = LL - math.log(total)
log_ratio = math.log2((a / c) / (b / d))
OR = (a / (c - a)) / (b / (d - b))
percent_diff = (((a / c) * 1000000 - (b / d) * 1000000) * 100) / ((b / d) * 1000000)

# Print results
print(f"E1: {E1:.20f}")
print(f"E2: {E2:.20f}")
print(f"LL: {LL:.20f}")
print(f"BIC: {BIC:.20f}")
print(f"Log Ratio: {log_ratio:.20f}")
print(f"Odds Ratio: {OR:.20f}")
print(f"%DIFF: {percent_diff:.20f}")
