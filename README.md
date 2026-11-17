# Financial Transaction Fraud Detection using Benford's Law

A Python-based financial anomaly detection tool that applies **Benford's Law** to transaction data to identify unusual numerical patterns that may warrant further fraud investigation.

The project compares the observed distribution of leading digits in financial transactions with the distribution predicted by Benford's Law.

> **Important:** Benford's Law does not prove that fraud has occurred. It is an analytical screening technique that can highlight unusual datasets or transactions for further investigation.

---

## Overview

Fraud detection in financial systems often involves identifying unusual patterns hidden within large volumes of transaction data.

Examples include:

- Accounts payable transactions
- Vendor invoices
- Expense claims
- Purchase transactions
- General ledger postings
- Insurance claims
- Reimbursements
- Payment records

Instead of defining individual transactions as fraudulent, Benford's Law can be used as an initial statistical screening mechanism.

If the distribution of digits in a suitable financial dataset deviates significantly from the expected Benford distribution, the dataset may deserve additional investigation.

This project demonstrates that concept using Python.

---

## What is Benford's Law?

Benford's Law, sometimes called the **First-Digit Law**, describes the frequency with which digits appear as the leading digit of numbers in many naturally occurring datasets.

A common assumption might be that the digits 1 through 9 should each occur as the first digit approximately 11.1% of the time.

In many real-world datasets, however, this is not what happens.

Numbers beginning with **1** occur much more frequently than numbers beginning with **9**.

According to Benford's Law, the probability that a number begins with digit `d` is:

```text
P(d) = log10(1 + 1/d)
```

where:

```text
d ∈ {1,2,3,4,5,6,7,8,9}
```

This produces approximately the following distribution:

| First Digit | Benford Expected Frequency |
|---:|---:|
| 1 | 30.10% |
| 2 | 17.61% |
| 3 | 12.49% |
| 4 | 9.69% |
| 5 | 7.92% |
| 6 | 6.69% |
| 7 | 5.80% |
| 8 | 5.12% |
| 9 | 4.58% |

The result is a decreasing logarithmic distribution.

---

## Why does this happen?

Many naturally occurring numerical datasets span multiple orders of magnitude.

For example, consider transaction amounts that can range from:

```text
10
50
100
750
1,500
8,000
25,000
150,000
```

When values grow naturally rather than being artificially assigned, numbers spend proportionally more time beginning with smaller digits.

As a consequence, numbers beginning with **1** frequently occur more often than numbers beginning with **8** or **9**.

This phenomenon has been observed across many kinds of naturally occurring numerical datasets.

---

## Benford's Law and Fraud Detection

Benford's Law has become an analytical technique used in areas such as:

- Forensic accounting
- Internal audit
- Financial auditing
- Fraud analytics
- Continuous controls monitoring
- Compliance analytics

The basic fraud-detection hypothesis is straightforward.

Naturally generated financial data may approximately follow Benford's Law. Numbers that are manually invented, manipulated, rounded, or artificially created may produce a different digit distribution.

For example, suppose an expense or invoice dataset contains an unusually large number of transactions beginning with the digit `9`.

Benford's Law expects approximately:

```text
9 → 4.58%
```

If the dataset instead contains:

```text
9 → 15%
```

that difference could be worth investigating.

This does **not** mean all transactions beginning with 9 are fraudulent.

Instead, the deviation acts as a statistical signal that can be combined with other fraud detection controls.

---

## Fraud Detection Workflow

A practical implementation could follow this process:

```text
Financial Transactions
         |
         v
Data Quality / Filtering
         |
         v
Extract Leading Digits
         |
         v
Calculate Actual Distribution
         |
         v
Calculate Benford Distribution
         |
         v
Compare Actual vs Expected
         |
         v
Calculate Deviation / MAD
         |
         v
Identify Anomalies
         |
         v
Detailed Fraud Investigation
```

Benford analysis therefore acts primarily as an **anomaly screening layer**.

---

## How This Project Works

The Python implementation performs the following steps.

### 1. Load transaction data

Financial values are read from:

```text
data.txt
```

Each line represents a transaction amount. Zero values are excluded from the analysis. Negative values are converted to their absolute magnitude before the first digit is analysed.

### 2. Extract the first significant digit

For each transaction, the first non-zero digit is extracted.

```text
125   → 1
348   → 3
1560  → 1
42    → 4
781   → 7
5680  → 5
```

The program counts how often each digit from 1 through 9 occurs.

### 3. Calculate the observed distribution

The percentage of transactions beginning with each digit is calculated:

```text
Observed frequency of digit 1 =
(Number of transactions beginning with 1 / Total transactions) × 100
```

### 4. Calculate the expected Benford distribution

For every first digit, the theoretical probability is calculated using:

```text
P(d) = log10(1 + 1/d)
```

Python implementation:

```python
percentage = math.log10(1 + (1 / digit)) * 100
```

### 5. Compare Actual vs Expected

For each digit, the program calculates the absolute difference between the actual frequency and the expected Benford frequency.

This makes it possible to identify which digits deviate most strongly from the expected distribution.

---

## Mean Absolute Deviation (MAD)

The implementation summarizes the overall difference using **Mean Absolute Deviation (MAD)**.

Conceptually:

```text
MAD = average(|Actual Frequency - Expected Frequency|)
```

A smaller MAD indicates that the dataset's first-digit distribution is closer to the expected Benford distribution.

A larger MAD indicates greater deviation.

---

## Current Proof-of-Concept Threshold

The current implementation uses the following demonstration logic:

```python
if mad < 5:
    conclusion = "Dataset broadly follows Benford's Law"
else:
    conclusion = "Dataset does NOT closely follow Benford's Law"
```

The `5` threshold should be understood as a **demonstration threshold used by this project**, rather than a universal fraud threshold.

A production implementation should use statistically justified conformity criteria together with sample-size considerations and domain-specific validation.

---

## Visualization

The project produces a visual comparison between:

- **Bars:** Actual transaction first-digit distribution
- **Red line:** Expected Benford distribution

If the bars are reasonably close to the Benford curve, the dataset broadly conforms to the expected distribution. Large or systematic differences may indicate numerical anomalies requiring additional investigation.

The generated visualization is stored as:

```text
benford_result.png
```

---

## Example Result

For the included demonstration dataset, the analysis produces a MAD of approximately:

**2.67%**

and reports:

**Dataset broadly follows Benford's Law**

This means the dataset does not show a strong first-digit anomaly according to the simple criterion implemented in this proof of concept.

It does **not** establish that every transaction is legitimate.

---

## Where Benford Analysis Can Be Applied

### Accounts Payable

Analyse vendor payments and invoice amounts for unusual digit distributions.

### Expense Fraud

Analyse employee expense claims for manually fabricated or manipulated amounts.

### Procurement

Analyse purchase orders and supplier transactions for unusual patterns.

### General Ledger

Apply Benford tests to selected accounting entries or journal postings.

### Insurance

Analyse claim amounts for statistical anomalies.

### Banking and Payments

Use Benford analysis as one feature within a broader transaction monitoring or anomaly-detection pipeline.

---

## Where Benford's Law Should NOT Be Used

Benford's Law does not apply equally well to every numerical dataset.

Problematic datasets can include:

- Sequential IDs
- Invoice numbers
- Customer numbers
- Telephone numbers
- Postal codes
- Randomly generated numbers
- Fixed-price transactions
- Data constrained to a narrow numerical range
- Values with artificial minimum or maximum limits

For example, analysing the *invoice amount* may be meaningful. Analysing the *invoice ID* usually is not.

Dataset suitability therefore needs to be evaluated before applying the test.

---

## Important Fraud Detection Limitation

Benford's Law should **not** be treated as a standalone fraud classifier.

Deviation from Benford's Law **does not prove fraud**, and conformity with Benford's Law **does not prove absence of fraud**.

A production fraud detection architecture should combine Benford analysis with other indicators such as:

- Transaction amount anomalies
- Transaction frequency
- Duplicate payments
- Vendor concentration
- New supplier activity
- Threshold avoidance
- Repeated rounded amounts
- Unusual transaction times
- Employee/vendor relationships
- Historical behavioural patterns
- Machine-learning anomaly scores

Benford's Law is therefore best considered an **analytical red-flag mechanism**.

---

## Example Enterprise Fraud Detection Architecture

```text
ERP / Banking / Payment Systems
             |
             v
      Transaction Data
             |
             v
     Data Quality Layer
             |
             v
   Fraud Feature Engineering
             |
    +--------+--------+
    |                 |
    v                 v
Benford Test     Rule-Based Tests
    |                 |
    +--------+--------+
             |
             v
   Anomaly Detection Model
             |
             v
       Risk Scoring
             |
             v
    Investigation Queue
             |
             v
    Fraud Analyst Review
```

This allows Benford deviation to become **one fraud-risk feature among many**, rather than making it the final decision mechanism.

---

## Technology

The proof of concept uses:

- Python
- Matplotlib
- Python `math` module
- Text-based transaction input

---

## Running the Project

### Clone the repository

```bash
git clone https://github.com/<username>/benford-fraud-detection.git
cd benford-fraud-detection
```

### Install dependency

```bash
pip install matplotlib
```

### Prepare transaction data

Place transaction amounts in `data.txt`, one amount per line.

### Run

```bash
python benford.py
```

The program:

1. Loads the transaction data
2. Extracts leading digits
3. Calculates observed frequencies
4. Generates the theoretical Benford distribution
5. Calculates MAD
6. Displays the analytical conclusion
7. Creates a visualization

Output:

```text
benford_result.png
```

---

## Suggested Repository Structure

```text
benford-fraud-detection/
│
├── README.md
├── benford.py
├── data/
│   └── sample_transactions.txt
├── output/
│   └── benford_result.png
├── requirements.txt
└── LICENSE
```

The original script should be renamed from `benson.py` to `benford.py`, because **Benford** is the correct name of the law.

---

## Future Improvements

- CSV and Excel transaction ingestion
- Pandas-based preprocessing
- First-two-digit Benford analysis
- Second-digit analysis
- Chi-square goodness-of-fit testing
- More rigorous MAD conformity thresholds
- Transaction-level anomaly identification
- Vendor-level Benford analysis
- Account-level analysis
- Time-window analysis
- Automated fraud risk scoring
- Interactive dashboard
- Power BI integration
- Databricks/Spark implementation for large transaction datasets
- Machine-learning anomaly detection
- Investigation workflow integration

---

## References

### Association of Certified Fraud Examiners (ACFE)

ACFE provides an accessible explanation of how Benford's Law can be used by fraud examiners to identify potentially suspicious numerical patterns:

- [What Is Benford's Law and Why Do Fraud Examiners Use It?](https://www.acfe.com/acfe-insights-blog/blog-detail?s=what-is-benfords-law-and-why-do-fraud-examiners-use-it)

### ACFE: Using Benford's Law to Detect Fraud

ACFE training material discusses first-digit, second-digit, first-two-digit, first-three-digit, and last-two-digit tests:

- [Using Benford's Law to Detect Fraud](https://cms.acfe.com/-/media/images/acfe/products/publication/self-study-cpe/workbook/using-benfords-law/using_benfords_law_sample.pdf)

### Mark J. Nigrini

Mark Nigrini is one of the best-known researchers and practitioners associated with applying Benford's Law to auditing and forensic accounting.

Recommended reference:

**Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection**, Mark J. Nigrini, Wiley.

---

## Disclaimer

This project is intended for educational, analytical, and proof-of-concept purposes.

Benford's Law identifies statistical anomalies and should not be used by itself to determine whether a transaction, employee, customer, or supplier is fraudulent.

Any anomalies identified by the model should be subjected to appropriate investigation and corroborated with additional financial, operational, and contextual evidence.
