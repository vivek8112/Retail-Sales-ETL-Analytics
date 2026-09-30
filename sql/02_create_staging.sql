USE RetailETL;
GO

CREATE TABLE dbo.stg_Customers (
    CustomerID INT,
    CustomerName VARCHAR(100),
    State VARCHAR(50),
    Segment VARCHAR(50)
);
GO

CREATE TABLE dbo.stg_Products (
    ProductID INT,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10,2),
    CostPrice DECIMAL(10,2)
);
GO

CREATE TABLE dbo.stg_Sales (
    SalesID INT,
    CustomerID INT,
    ProducrID INT,
    OrderDate DATE,
    Quantity INT
);
GO