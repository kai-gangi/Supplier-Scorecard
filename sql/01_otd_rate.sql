SELECT
    Supplier,
    COUNT(*) AS delivered_orders,
    SUM(CASE
        WHEN JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date) <= 30
        THEN 1 ELSE 0
    END) AS on_time,
    ROUND(100.0 * SUM(CASE
        WHEN JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date) <= 30
        THEN 1 ELSE 0
    END) / COUNT(*), 2) AS otd_rate
FROM orders
WHERE Order_Status = 'Delivered'
AND Delivery_Date != ''
GROUP BY Supplier;
