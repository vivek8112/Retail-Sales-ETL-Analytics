USE RetailETL;
GO

-- 1. Validate Product IDs in staging sales
SELECT s.*
FROM dbo.stg_Sales AS s
LEFT JOIN dbo.stg_Products AS p
    ON s.ProducrID = p.ProductID
WHERE p.ProductID IS NULL;
GO


-- 2. Validate FactSales row count
SELECT COUNT(*) AS TotalSalesRows
FROM dbo.FactSales;
GO


-- 3. Validate overall sales metrics
SELECT
    COUNT(*) AS TotalSalesRows,
    SUM(fs.Quantity) AS TotalQuantity,
    SUM(fs.Quantity * p.UnitPrice) AS TotalRevenue,
    SUM(fs.Quantity * p.CostPrice) AS TotalCost,
    SUM(fs.Quantity * (p.UnitPrice - p.CostPrice)) AS TotalProfit
FROM dbo.FactSales AS fs
INNER JOIN dbo.DimProduct AS p
    ON fs.ProductID = p.ProductID;
GO