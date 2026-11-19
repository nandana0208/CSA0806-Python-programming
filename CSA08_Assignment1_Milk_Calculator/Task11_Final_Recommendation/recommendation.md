# Task 11 – Recommend and Defend the Final Design

Recommend Decimal values constructed from input strings for litres, percentages and money. Use Decimal step arithmetic and explicit ROUND_HALF_UP; quantise every payable entry to Rs 0.01 and sum the rounded payments. Integer paise is another exact option if all intermediate values can be converted under a documented rounding policy.

Keep the rate card in one module or external configuration file. A revision should update one versioned rate card, be covered by tests, and record its effective date. Validate farmer ID, positive quantity, fat limits, shift and configured SNF limits. Retain collection records for audit and correction.

For one centre, a Python list and loop are sufficient. At district scale (150,000 farmers, multiple shifts and dates), the arithmetic remains O(n), but the system should persist entries in a database, index farmer/date, validate imports in batches, back up data and produce reconciliation reports. The calculator's numeric design remains correct; operational architecture should be expanded.

Limitations: official SNF bounds, date/period definitions, tie policy and seasonal effective-date rules must be approved by the co-operative. A JSON rate card would make seasonal updates possible without editing source code, but requires schema validation, versioning and secure change control. Loading t rate values costs O(t) time and O(t) memory at start-up, usually tiny compared with the benefit of controlled rate revisions.
