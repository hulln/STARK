# Collocation Measures

Collocation metrics are statistical tools used to evaluate the strength of association between words in a corpus. They compare the observed frequency of a word pair (or n-gram) with its expected frequency under the assumption of independence. Below are several common collocation metrics along with their corresponding equations.

## Given Data

- $c(w_1 \ldots w_n)$: Frequency of the n-gram (e.g., the frequency of `t. i.` together)
- $c(w_1)$: Frequency of the first word (e.g., `t.`)
- $c(w_n)$: Frequency of the $n$-th word (e.g., `i.`)
- $N$: Total number of words in the corpus
- $n$: Length of the n-gram (for a bigram, $n = 2$)

## Expected Frequency

The expected frequency of the n-gram is computed as:

$$
E(w_1 \ldots w_n) \approx \frac{c{(w_1) \ldots c(w_n)}}{N^{(n-1)}}
$$

For a bigram ($n = 2$), this simplifies to:

$$
E(w_1w_2) = \frac{c_{w_1} \times c_{w_2}}{N}
$$

## Collocation Measures and Their Equations
[Collocations in Corpus-Based Language Learning Research: Identifying, Comparing, and Interpreting the Evidence](https://onlinelibrary.wiley.com/doi/10.1111/lang.12225)


| **Measure**                          | **Equation**                                                                                                                                                                   |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[Mutual Information (MI)](https://wordbanks.harpercollins.co.uk/other_doc/statistics.html)**         | $\displaystyle \text{MI} = \log_2\!\left(\frac{c(w_1 \ldots w_n)}{E(w_1 \ldots w_n)}\right)$                                                                                           |
| **MI³**                           | $\displaystyle \text{MI}^3 = \log_2\!\left(\frac{c(w_1 \ldots w_n)^3}{E(w_1 \ldots w_n)}\right)$                                                                                         |
| **Dice Coefficient**                | $\displaystyle \text{Dice} = \frac{n \times c(w_1 \ldots w_n)}{\sum_{i=1}^{n} c(w_i)}$                                                                                                   |
| **[log-Dice](https://www.sketchengine.eu/glossary/logdice/)**                        | $\displaystyle \text{logDice} = 14 + \log_2\!\left(\text{Dice}\right)$                                                                                                            |
| **[t-score](https://wordbanks.harpercollins.co.uk/other_doc/statistics.html)**                          | $\displaystyle \text{t-score} = \frac{c(w_1 \ldots w_n) - E(w_1 \ldots w_n)}{\sqrt{c(w_1 \ldots w_n)}}$                                                                                          |
| **Simple Log-Likelihood (LL)**      | $\text{LL} = 2 \times \left(c(w_1 \ldots w_n) \log_{10}\!\left(\frac{c(w_1 \ldots w_n)}{E(w_1 \ldots w_n)}\right) - \Bigl(c(w_1 \ldots w_n) - E(w_1 \ldots w_n)\Bigr)\right)$  |
