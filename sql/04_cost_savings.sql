SELECT
    Supplier,
    ROUND(SUM((Unit_Price - Negotiated_Price) * Quantity), 2) AS total_savings,
    ROUND(100.0 * AVG((Unit_Price - Negotiated_Price) / Unit_Price), 2) AS avg_savings_pct
FROM orders
GROUP BY Supplier;
