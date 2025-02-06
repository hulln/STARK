import math

# Given values
a = RFC1 = 2
b = RFC2 = 0.000000000000000001
c = C1 = 267097
d = C2 = 400391

NFC1 = a / c
NFC2 = b / d

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

# Double-check results with formulas from article
# Calculate Log Ratio with normalized frequencies
log_ratio_2 = math.log2((NFC1) / (NFC2))
print(f"Log Ratio 2: {log_ratio_2:.20f}")

# Calculate OR with normalized frequencies
OR_2 = (RFC1 / (C1 - RFC1)) / (RFC2 / (C2 - RFC2))
print(f"Odds Ratio 2: {OR_2:.20f}")

# Calculate %DIFF with normalized frequencies
percent_diff_2 = ((NFC1 - NFC2) * 100) / NFC2
print(f"%DIFF 2: {percent_diff_2:.20f}")

print(a, RFC1, b, RFC2, c, C1, d, C2)