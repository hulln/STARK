# Keyness Measures

Keyness measures are statistical tools that compare the frequency of words in a target corpus with that in a reference corpus to highlight distinctive vocabulary. Despite the use of different metrics (e.g., Log Ratio, Odds Ratio, %DIFF), they tend to produce very similar rankings of keywords ([Keyness analysis: Nature, metrics and techniques](https://www.researchgate.net/publication/319208347_Keyness_analysis_Nature_metrics_and_techniques)).

- **[LL (Log-Likelihood)](https://ucrel.lancs.ac.uk/llwizard.html):** Measures the statistical significance of frequency differences.
- **[BIC (Bayesian Information Criterion)](https://core.ac.uk/download/pdf/227092349.pdf):** Adjusted LL with a complexity penalty.
- **[Log Ratio](https://cass.lancs.ac.uk/log-ratio-an-informal-introduction/):** Measures the relative strength of frequency differences.
- **[Odds Ratio (OR)](http://crs2.kmutt.ac.th/Key-BNC/):** Compares the likelihood of occurrence between corpora.
- **[%DIFF](https://core.ac.uk/download/pdf/227092349.pdf):** The percentage difference in normalized frequencies.

## Data
### Given Data

| **Term**              | **Meaning**                                                                                     | **Example**                                                                 |
|-----------------------|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **$a = \text{RFC}_1$** | Absolute (raw) frequency of the n-gram in **Corpus 1**.                                         | If `t. i.` appears 50 times in Corpus 1, then $a = 50$.                     |
| **$b = \text{RFC}_2$** | Absolute (raw) frequency of the n-gram in **Corpus 2** (set to `0.000000000000000001` if none). | If `t. i.` appears 30 times in Corpus 2, then $b = 30$. If absent, $b = 0.000000000000000001$. |
| **$c = \text{C}_1$**   | Total number of **tokens** (words) in **Corpus 1**.                                             | If Corpus 1 has 1,000,000 words, then $c = 1,000,000$.                       |
| **$d = \text{C}_2$**   | Total number of **tokens** (words) in **Corpus 2**.                                             | If Corpus 2 has 800,000 words, then $d = 800,000$.                           |


### Normalized Frequencies
Normalized frequencies ($ \text{NFC}_1 $ and $ \text{NFC}_2 $) are calculated by dividing the frequency by the total corpus size:

$$ \text{NFC}_1 = \frac{a}{c} = \frac{\text{RFC}_1}{\text{C}_1}, \quad \text{NFC}_2 = \frac{b}{d} = \frac{\text{RFC}_2}{\text{C}_2} $$

### Expected Frequencies

Expected frequencies $ E_1 $ and $ E_2 $ are computed as:

$$ E_1 = \frac{c (a + b)}{c + d}, \quad E_2 = \frac{d (a + b)}{c + d} $$

## Keyness Equations
### Log-Likelihood (LL)

$$ \text{LL} = 2 \times \left( a \log\left(\frac{a}{E_1}\right) + b \log\left(\frac{b}{E_2}\right) \right) $$

### Bayesian Information Criterion (BIC)

$$ \text{BIC} = \text{LL} - \log(c + d) $$

### Log Ratio

$$ \text{Log Ratio} = \log_2 \left(\frac{\frac{a}{c}}{\frac{b}{d}}\right) = \log_2 \left(\frac{\text{NFC}_1}{\text{NFC}_2}\right) $$

### Odds Ratio (OR)

$$ \text{OR} = \frac{\frac{a}{c - a}}{\frac{b}{d - b}} = \frac{\text{RFC}_1/(\text{C}_1 - \text{RFC}_1)}{\text{RFC}_2/(\text{C}_2 - \text{RFC}_2)} $$

### Percentage Difference (%DIFF)

$$ \%\text{DIFF} = \frac{\left( \frac{a}{c} \times 10^6 - \frac{b}{d} \times 10^6 \right) \times 100}{\frac{b}{d} \times 10^6} = \frac{(\text{NFC}_1 - \text{NFC}_2) \times 100}{\text{NFC}_2} $$

# Summary
| **Metric**         | **Equation**                                                                                                                                               |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| $\text{LL}$        | $2 \times \left( a \log\left(\frac{a}{E_1}\right) + b \log\left(\frac{b}{E_2}\right) \right)$                                                                |
| $\text{BIC}$       | $\text{LL} - \log(c + d)$                                                                                                                                   |
| $\text{Log Ratio}$ | $\log_2 \left(\frac{\text{NFC}_1}{\text{NFC}_2}\right)$                                                                                                      |
| $\text{OR}$        | $\frac{\text{RFC}_1/(\text{C}_1 - \text{RFC}_1)}{\text{RFC}_2/(\text{C}_2 - \text{RFC}_2)}$                                                                                                                   |
| $\%\text{DIFF}$    | $\frac{(\text{NFC}_1 - \text{NFC}_2) \times 100}{\text{NFC}_2}$                                                                                              |
