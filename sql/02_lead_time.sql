SELECT
    Supplier,
    ROUND(AVG(JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date)), 1) AS avg_lead_time_days,
    ROUND(MIN(JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date)), 1) AS min_lead_time,
    ROUND(MAX(JULIANDAY(Delivery_Date) - JULIANDAY(Order_Date)), 1) AS max_lead_time
FROM orders
WHERE Order_Status = 'Delivered'
AND Delivery_Date != ''
GROUP BY Supplier;
