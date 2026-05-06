SELECT
    Supplier,
    ROUND(SUM(Defective_Units), 0) AS total_defects,
    ROUND(SUM(Quantity), 0) AS total_units,
    ROUND(100.0 * SUM(Defective_Units) / SUM(Quantity), 2) AS defect_rate_pct
FROM orders
WHERE Defective_Units != ''
GROUP BY Supplier;
