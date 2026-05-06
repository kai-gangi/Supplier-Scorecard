SELECT
    Supplier,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN Compliance = 'Yes' THEN 1 ELSE 0 END) AS compliant_orders,
    ROUND(100.0 * SUM(CASE WHEN Compliance = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS compliance_rate
FROM orders
GROUP BY Supplier;
