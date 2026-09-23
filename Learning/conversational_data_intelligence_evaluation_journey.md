# Evaluation Journey — Conversational Data Intelligence

## Purpose

This document captures the evaluation work performed during Phase 1 of the Conversational Data Intelligence project.

The interview story is simple: we did not stop when NL-to-SQL produced plausible answers. We built a repeatable evaluation set, inspected generated SQL and database results, found failure modes, and iteratively improved the system.

## 1. Evaluation Setup

We created 8 representative business questions:

1. Which city has the most customers?
2. How many orders are currently delivered?
3. Which product category has the highest number of orders?
4. How many customers are there in Sao Paulo?
5. Which order status has the most orders?
6. How many products are in the products table?
7. Which product category has the most products?
8. How many orders contain more than one item?

Files:

```text
tests/
├── __init__.py
├── evaluation_questions.json
└── run_evaluation.py
```

The real `ask_data_agent()` pipeline is evaluated:

```text
Question
   ↓
LLM SQL Generation
   ↓
SQL Validation
   ↓
SQLite Execution
   ↓
Answer Generation
   ↓
Evaluation
```

We first printed SQL, database results, and the final answer. We then evolved the runner to compare actual database results against expected results.

## 2. Why We Compare Results Instead of Exact SQL

We deliberately do not compare SQL strings. Multiple SQL queries can correctly answer the same business question.

Therefore:

```text
Generated SQL
      ↓
Database
      ↓
Actual result
      ↓
Compare with expected result
```

This evaluates semantic/business correctness rather than whether the model produced one exact SQL formulation.

## 3. Initial Baseline

The first structured evaluation produced:

```text
Passed: 6
Failed: 2
Total:  8
```

Pass rate:

```text
75%
```

Two important failure modes were identified.

## 4. Failure — City vs State / Case Sensitivity

Question:

```text
How many customers are there in Sao Paulo?
```

An initial query used:

```sql
WHERE customer_city = 'Sao Paulo'
```

The database stores the city as:

```text
sao paulo
```

so the query returned:

```text
0
```

We first added this SQL-generation rule:

```text
For text comparisons, use case-insensitive matching when appropriate,
such as LOWER(column) = LOWER(value).
```

The model then produced:

```sql
WHERE LOWER(customer_state) = LOWER('São Paulo')
```

This still returned 0.

That exposed a second, deeper problem: **semantic column selection**. The model selected `customer_state` even though the user asked for a city.

### Fix

We added semantic guidance:

```text
Match the user's wording to the correct semantic column.
For example, "city" must use a city column, while "state" must use a state column.

Do not substitute one geographic attribute for another.
If the user asks about a city, do not use a state column.
```

The model then generated:

```sql
SELECT COUNT(DISTINCT customer_id) AS num_customers
FROM customers
WHERE LOWER(customer_city) = LOWER('Sao Paulo');
```

Result:

```text
15,540
```

The question passed.

## 5. Failure — Business Semantics of "Delivered"

Question:

```text
How many orders are currently delivered?
```

Our evaluation ground truth was:

```text
96,478
```

A query using:

```sql
WHERE order_status = 'delivered'
```

returned:

```text
96,478
```

However, the model also generated interpretations based on:

```sql
order_delivered_customer_date IS NOT NULL
```

which returned:

```text
96,476
```

and at one point combined the two conditions with `OR`, returning:

```text
96,484
```

This exposed a different class of problem: **business-semantic ambiguity**.

The SQL was valid and executable, but the model was interpreting "delivered" differently.

## 6. Evaluation After Semantic Prompt Improvements

After adding guidance for:

- Case-insensitive text matching
- City vs state semantics
- Order status vs delivery-date semantics

the evaluation improved to:

```text
Passed: 7
Failed: 1
Total: 8
Pass rate: 87.5%
```

The city problem was fixed.

The remaining failure was still:

```text
How many orders are currently delivered?
```

Latest observed interpretation:

```sql
WHERE order_delivered_customer_date IS NOT NULL
```

Actual:

```text
96,476
```

Expected:

```text
96,478
```

We have intentionally not hard-coded a question-specific answer.

## 7. Failure Classes We Discovered

### A. Data normalization

Example:

```text
"Sao Paulo"
vs
"sao paulo"
```

Technique:

```sql
LOWER(column) = LOWER(value)
```

### B. Schema/column semantics

Example:

```text
User asks for CITY
        ↓
Model selects STATE
```

This indicates that simply providing a schema is not always enough; the system needs stronger understanding of column meaning.

### C. Business semantics

Example:

```text
"delivered orders"
```

could involve:

```text
order_status
```

or:

```text
order_delivered_customer_date
```

This demonstrates that syntactically valid SQL can still be semantically wrong for the intended business definition.

## 8. Current Evaluation Status

Latest measured result:

```text
Total questions: 8
Passed:          7
Failed:          1
Pass rate:       87.5%
```

Remaining issue:

```text
How many orders are currently delivered?
```

Expected:

```text
96,478
```

Latest generated interpretation:

```text
order_delivered_customer_date IS NOT NULL
```

Actual:

```text
96,476
```

The next engineering step is to inspect the underlying data/business semantics and determine how the agent should distinguish order status from delivery-date information.

## 9. Interview Explanation

A concise version:

> "After building the initial NL-to-SQL pipeline, I didn't just test whether the API returned an answer. I created an evaluation set of representative business questions and ran them through the actual agent. Initially, 6 out of 8 passed. One failure exposed case-sensitive matching, and another exposed incorrect semantic column selection — the model interpreted a city as a state. I improved the SQL-generation instructions to use case-insensitive matching and map user terminology to the correct schema semantics. That brought the evaluation to 7 out of 8. The remaining failure exposed a deeper business-semantic ambiguity around what 'delivered' means in the dataset. That showed me that reliable NL-to-SQL requires more than syntactically valid SQL — it needs schema understanding, business semantics, and systematic evaluation."

## 10. Interview Follow-ups

### Why create an evaluation framework?

> "LLM applications are probabilistic. A single successful query doesn't establish reliability. I wanted repeatable tests that could detect regressions and expose failure modes."

### Why compare results instead of SQL?

> "There can be multiple valid SQL formulations for the same business question. I care about semantic correctness of the result rather than exact SQL-string matching."

### What did the evaluation teach you?

> "It showed me that SQL generation can fail even when the SQL is syntactically valid. We encountered data normalization issues, schema semantic errors, and business-meaning ambiguity."

### What would you improve next?

> "I would introduce stronger schema intelligence so the model can explicitly identify relevant tables, columns, relationships and their meanings before generating SQL. I'd also add result validation and controlled SQL correction for cases where the generated query doesn't satisfy the question."

## 11. Engineering Pattern

The key development loop is:

```text
Build
  ↓
Test
  ↓
Measure
  ↓
Find failure
  ↓
Understand root cause
  ↓
Improve
  ↓
Re-evaluate
```

This is the evaluation-driven development approach being used for the conversational data intelligence system.
