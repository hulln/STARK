# Collocation Measures

Collocation metrics are statistical tools used to evaluate the strength of association between words in a corpus. They compare the observed frequency of a word pair (or n-gram) with its expected frequency under the assumption of independence. Below are several common collocation metrics along with their corresponding equations.

## Given Data

| **Term**               | **Meaning**                                                                                                   | **Example**                                                                 |
|------------------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **$c(w_1 \ldots w_n)$** | Frequency of the entire n-gram (observed co-occurrence of the sequence).                                      | Frequency of `t. i.` together in the corpus.                               |
| **$c(w_i)$**            | Frequency of the **$i$-th word** in the n-gram (where $i = 1, 2, \ldots, n$).                                 | - $c(w_1)$ = frequency of `t.` (first word).<br>- $c(w_2)$ = frequency of `i.` (second word). |
| **$N$**                 | Total number of **tokens** (words) in the corpus.                                                             | If the corpus has 1,000,000 words, $N = 1,000,000$.                        |
| **$n$**                 | Length of the n-gram (number of words in the sequence).                                                       | For a bigram (`t. i.`), $n = 2$.                                            |

## Expected Frequency

The expected frequency of the n-gram is computed as:

$$
E(w_1 \ldots w_n) \approx \frac{c{(w_1) \ldots c(w_n)}}{N^{(n-1)}}
$$

For a bigram ($n = 2$), this simplifies to:

$$
E(w_1w_2) = \frac{c_{w_1} \times c_{w_2}}{N}
$$

## Collocation Measures and Equations
[Collocations in Corpus-Based Language Learning Research: Identifying, Comparing, and Interpreting the Evidence](https://onlinelibrary.wiley.com/doi/10.1111/lang.12225)


| **Measure**                          | **Equation**                                                                                                                                                                   |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[Mutual Information (MI)](https://wordbanks.harpercollins.co.uk/other_doc/statistics.html)**         | $\displaystyle \text{MI} = \log_2\left(\frac{c(w_1 \ldots w_n)}{E(w_1 \ldots w_n)}\right)$                                                                                           |
| **MI³**                           | $\displaystyle \text{MI}^3 = \log_2\left(\frac{c(w_1 \ldots w_n)^3}{E(w_1 \ldots w_n)}\right)$                                                                                         |
| **Dice Coefficient**                | $\displaystyle \text{Dice} = \frac{n \times c(w_1 \ldots w_n)}{\sum_{i=1}^{n} c(w_i)}$                                                                                                   |
| **[log-Dice](https://www.sketchengine.eu/glossary/logdice/)**                        | $\displaystyle \text{logDice} = 14 + \log_2\left(\text{Dice}\right)$                                                                                                            |
| **[t-score](https://wordbanks.harpercollins.co.uk/other_doc/statistics.html)**                          | $\displaystyle \text{t-score} = \frac{c(w_1 \ldots w_n) - E(w_1 \ldots w_n)}{\sqrt{c(w_1 \ldots w_n)}}$                                                                                          |
| **Simple Log-Likelihood (LL)**      | $\text{LL} = 2 \times \left(c(w_1 \ldots w_n) \log_{10}\left(\frac{c(w_1 \ldots w_n)}{E(w_1 \ldots w_n)}\right) - \Bigl(c(w_1 \ldots w_n) - E(w_1 \ldots w_n)\Bigr)\right)$  |
