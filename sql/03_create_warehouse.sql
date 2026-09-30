USE RetailETL;
GO

CREATE TABLE dbo.DimCustomer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(100),
    State VARCHAR(50),
    Segment VARCHAR(50)
);
GO

CREATE TABLE dbo.DimProduct (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(50),
    UnitPrice DECIMAL(10,2),
    CostPrice DECIMAL(10,2)
);
GO

CREATE TABLE dbo.DimDate (
    [Date] DATE PRIMARY KEY,
    [Year] INT,
    [Month] INT,
    MonthName VARCHAR(20)
);
GO

CREATE TABLE dbo.FactSales (
    SalesID INT PRIMARY KEY,
    CustomerID INT,
    ProductID INT,
    OrderDate DATE,
    Quantity INT,

    FOREIGN KEY (CustomerID)
        REFERENCES dbo.DimCustomer(CustomerID),

    FOREIGN KEY (ProductID)
        REFERENCES dbo.DimProduct(ProductID),

    FOREIGN KEY (OrderDate)
        REFERENCES dbo.DimDate([Date])
);
GO