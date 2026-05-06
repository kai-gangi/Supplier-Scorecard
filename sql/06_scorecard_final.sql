SELECT
    o.Supplier,
    otd.otd_rate,
    lt.avg_lead_time_days,
    d.defect_rate_pct,
    cs.avg_savings_pct,
    co.compliance_rate,
    ROUND(
        (otd.otd_rate * 0.35) +
        ((100 - d.defect_rate_pct) * 0.25) +
        (co.compliance_rate * 0.20) +
        (cs.avg_savings_pct * 0.10) +
        ((100 - lt.avg_lead_time_days) * 0.10),
    2) AS weighted_score
FROM (SELECT DISTINCT Supplier FROM orders) o
LEFT JOIN (
    SELECT Supplier,
    ROUND(100.0 * SUM(CASE WHEN JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date) <= 30 THEN 1 ELSE 0 END) / COUNT(*), 2) AS otd_rate
    FROM orders WHERE Order_Status = 'Delivered' AND Delivery_Date != ''
    GROUP BY Supplier
) otd ON o.Supplier = otd.Supplier
LEFT JOIN (
    SELECT Supplier,
    ROUND(AVG(JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date)), 1) AS avg_lead_time_days
    FROM orders WHERE Order_Status = 'Delivered' AND Delivery_Date != ''
    GROUP BY Supplier
) lt ON o.Supplier = lt.Supplier
LEFT JOIN (
    SELECT Supplier,
    ROUND(100.0 * SUM(Defective_Units) / SUM(Quantity), 2) AS defect_rate_pct
    FROM orders WHERE Defective_Units != ''
    GROUP BY Supplier
) d ON o.Supplier = d.Supplier
LEFT JOIN (
    SELECT Supplier,
    ROUND(100.0 * AVG((Unit_Price - Negotiated_Price) / Unit_Price), 2) AS avg_savings_pct
    FROM orders GROUP BY Supplier
) cs ON o.Supplier = cs.Supplier
LEFT JOIN (
    SELECT Supplier,
    ROUND(100.0 * SUM(CASE WHEN Compliance = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS compliance_rate
    FROM orders GROUP BY Supplier
) co ON o.Supplier = co.Supplier
ORDER BY weighted_score DESC;
