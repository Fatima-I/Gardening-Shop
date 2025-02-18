create database db_nursery2

CREATE TABLE tbl_Type (
    Type_ID INT PRIMARY KEY,
    Type_Name VARCHAR(20) NOT NULL
);
INSERT INTO tbl_Type (Type_ID, Type_Name) VALUES
(1, 'Seeds'),
(2, 'Plants'),
(3, 'Tools'),
(4, 'Fertilizers');
select * from tbl_Type


CREATE TABLE tbl_Category (
    Category_ID INT PRIMARY KEY,
    Category_Name VARCHAR(20) NOT NULL,
    Type_ID INT FOREIGN KEY REFERENCES tbl_Type(Type_ID)
);
INSERT INTO tbl_Category (Category_ID, Category_Name, Type_ID) VALUES
(1, 'Vegetable Seeds', 1),
(2, 'Flowering Plants', 2),
(3, 'Hand Tools', 3),
(4, 'Chemical Fertilizers', 4);
select * from tbl_Category

CREATE TABLE tbl_Sub_Category (
    Sub_Category_ID INT PRIMARY KEY,
    Sub_Category_Name VARCHAR(20) NOT NULL,
    Category_ID INT FOREIGN KEY REFERENCES tbl_Category(Category_ID)
);
INSERT INTO tbl_Sub_Category (Sub_Category_ID, Sub_Category_Name, Category_ID) VALUES
(1, 'Winter Vegetables', 1),
(2, 'Summer Vegetables', 1),
(3, 'Indoor Plants', 2),
(4, 'Outdoor Plants', 2);
select * from tbl_Sub_Category

CREATE TABLE tbl_Purchase (
    Purchase_ID INT PRIMARY KEY,
    Purchase_Date DATE NOT NULL
);
INSERT INTO tbl_Purchase (Purchase_ID, Purchase_Date) VALUES
(1, '2024-12-01'),
(2, '2024-12-02'),
(3, '2024-12-03'),
(4, '2024-12-04');
select * from tbl_Purchase

CREATE TABLE tbl_Sale (
    Sale_ID INT PRIMARY KEY,
    Sale_Date DATE NOT NULL
);

INSERT INTO tbl_Sale (Sale_ID, Sale_Date) VALUES
(1, '2024-12-05'),
(2, '2024-12-06'),
(3, '2024-12-07'),
(4, '2024-12-08');
select * from tbl_Sale

CREATE TABLE tbl_Product (
    Product_ID INT PRIMARY KEY,
    Product_Name VARCHAR(20) NOT NULL,
    Type_ID INT FOREIGN KEY REFERENCES tbl_Type(Type_ID),
    Category_ID INT FOREIGN KEY REFERENCES tbl_Category(Category_ID),
    Quantity INT NOT NULL,
    Price FLOAT NOT NULL,
    Shelf_Life FLOAT NOT NULL,
);
INSERT INTO tbl_Product (Product_ID, Product_Name, Type_ID, Category_ID, Quantity, Price, Shelf_Life) VALUES
(1, 'Tomato Seeds', 1, 1, 100, 2.50, 12),
(2, 'Rose Plant', 2, 2, 50, 150.00, 24),
(3, 'Pruning Shears', 3, 3, 30, 75.00, 0),
(4, 'Urea Fertilizer', 4, 4, 200, 25.00, 36);

CREATE TABLE tbl_Product_And_Sub_Category (
    Product_ID INT FOREIGN KEY REFERENCES tbl_Product(Product_ID),
    Sub_Category_ID INT FOREIGN KEY REFERENCES tbl_Sub_Category(Sub_Category_ID)
    PRIMARY KEY (Product_ID, Sub_Category_ID),
);

INSERT INTO tbl_Product_And_Sub_Category (Product_ID, Sub_Category_ID) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4);

CREATE TABLE tbl_Product_And_Purchase (
    Product_ID INT FOREIGN KEY REFERENCES tbl_Product(Product_ID),
    Purchase_ID INT FOREIGN KEY REFERENCES tbl_Purchase(Purchase_ID),
    QuantityPurchased INT NOT NULL,
    Purchasing_Price FLOAT NOT NULL,
    Selling_Price FLOAT,
    PRIMARY KEY (Product_ID, Purchase_ID),
);

INSERT INTO tbl_Product_And_Purchase (Product_ID, Purchase_ID, QuantityPurchased, Purchasing_Price, Selling_Price) VALUES
(1, 1, 50, 1.50, 2.50),
(2, 2, 20, 100.00, 150.00),
(3, 3, 15, 50.00, 75.00),
(4, 4, 100, 20.00, 25.00);

CREATE TABLE tbl_Product_And_Sale (
    Product_ID INT FOREIGN KEY REFERENCES tbl_Product(Product_ID),
    Sale_ID INT FOREIGN KEY REFERENCES tbl_Sale(Sale_ID),
    QuantitySaled INT NOT NULL,
    PRIMARY KEY (Product_ID, Sale_ID), 
);

ALTER TABLE tbl_Product_And_Sale
ADD Sale_Price DECIMAL(10, 2) NOT NULL;

INSERT INTO tbl_Product_And_Sale (Product_ID, Sale_ID, QuantitySaled, Sale_Price) VALUES
(1, 1, 10,50),
(2, 2, 5,100),
(3, 3, 3,600),
(4, 4, 20,78);

CREATE TABLE tbl_pricehistory (
    Product_ID INT FOREIGN KEY REFERENCES tbl_Product(Product_ID),
    Updation_Date DATE NOT NULL,
    Updated_Price FLOAT NOT NULL,
    PRIMARY KEY (Product_ID, Updation_Date), 
);

ALTER TABLE tbl_pricehistory
DROP CONSTRAINT [PK__tbl_pric__D747F5668CFC4031];

ALTER TABLE tbl_pricehistory
ADD CONSTRAINT [PK__tbl_pric__D747F5668CFC4031] PRIMARY KEY (Product_ID, Updation_Date, Updated_Price);

select * from tbl_Product
select * from tbl_Category
select * from tbl_Type
select * from tbl_Sub_Category
select * from tbl_Product_And_Sub_Category
select * from tbl_Purchase
select * from tbl_Product_And_Purchase
select * from tbl_Product_And_Sale
select * from tbl_Sale
select * from tbl_pricehistory

TRUNCATE TABLE tbl_Product_And_Sale

ALTER TABLE tbl_Product_And_Sale
ADD Sale_Price DECIMAL(10, 2) NOT NULL;

CREATE OR ALTER PROCEDURE last_insert_id
AS
BEGIN
    SELECT max(Product_ID) from tbl_Product
END
GO



select Product_ID, Product_Name, Quantity, Price, Shelf_Life from tbl_Product
select *, (select name from department d where s.departmentID = d.departmentID) as dname 
from student s 
where (select name from department d where s.departmentID = d.departmentID) is not null

insert into tbl_Product (Product_Name, Quantity, Price, Shelf_Life) values ()
insert into tbl_Product (Type_ID) values

CREATE OR ALTER PROCEDURE InsertProductAndLinkSubcategory
    @ProductID INT,
    @ProductName NVARCHAR(255),
    @TypeName NVARCHAR(255),
    @CategoryName NVARCHAR(255),
    @SubCategoryName NVARCHAR(255),
    @Quantity INT,
    @Price DECIMAL(18, 2),
    @ShelfLife INT
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @TypeID INT, @CategoryID INT, @SubCategoryID INT, @ProductExists INT;

        -- Check if the product already exists in tbl_Product
        SELECT @ProductExists = COUNT(*)
        FROM tbl_Product
        WHERE Product_Name = @ProductName;

        IF @ProductExists > 0
        BEGIN
            THROW 50003, 'Product already exists in tbl_Product.', 1;
        END

        -- Get Type_ID based on Type_Name
        SELECT @TypeID = Type_ID 
        FROM tbl_Type 
        WHERE Type_Name = @TypeName;

        IF @TypeID IS NULL
        BEGIN
            THROW 50000, 'Type not found in tbl_Type.', 1;
        END

        -- Get Category_ID based on Category_Name
        SELECT @CategoryID = Category_ID 
        FROM tbl_Category 
        WHERE Category_Name = @CategoryName;

        IF @CategoryID IS NULL
        BEGIN
            THROW 50001, 'Category not found in tbl_Category.', 1;
        END

        -- Get Sub_Category_ID based on Sub_Category_Name
        SELECT @SubCategoryID = Sub_Category_ID 
        FROM tbl_Sub_Category 
        WHERE Sub_Category_Name = @SubCategoryName;

        IF @SubCategoryID IS NULL
        BEGIN
            THROW 50002, 'Subcategory not found in tbl_Sub_Category.', 1;
        END

        -- Insert into tbl_Product
        INSERT INTO tbl_Product (Product_ID, Product_Name, Type_ID, Category_ID, Quantity, Price, Shelf_Life)
        VALUES (@ProductID, @ProductName, @TypeID, @CategoryID, @Quantity, @Price, @ShelfLife);

        -- Insert into tbl_Product_And_Sub_Category
        INSERT INTO tbl_Product_And_Sub_Category (Product_ID, Sub_Category_ID)
        VALUES (@ProductID, @SubCategoryID);

        -- Success message
        PRINT 'Product and subcategory link inserted successfully.';

    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT;
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END

CREATE OR ALTER PROCEDURE InsertCategory
    @CategoryID INT,
    @CategoryName NVARCHAR(255),
    @TypeName NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @TypeID INT;

        -- Get Type_ID based on Type_Name
        SELECT @TypeID = Type_ID 
        FROM tbl_Type 
        WHERE Type_Name = @TypeName;

        IF @TypeID IS NULL
        BEGIN
            THROW 50000, 'Type not found in tbl_Type.', 1;
        END

        -- Check for duplicate Category_Name
        IF EXISTS (SELECT 1 FROM tbl_Category WHERE Category_Name = @CategoryName)
        BEGIN
            THROW 50001, 'Category already exists in tbl_Category.', 1;
        END

        -- Insert into tbl_Category
        INSERT INTO tbl_Category (Category_ID, Category_Name, Type_ID)
        VALUES (@CategoryID, @CategoryName, @TypeID);

        -- Success message
        PRINT 'Category added successfully.';

    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT;
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END

CREATE OR ALTER PROCEDURE InsertSubCategory
    @SubCategoryID INT,
	@SubCategoryName NVARCHAR(255),
    @CategoryName NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @CategoryID INT;

		-- Get Category_ID based on Category_Name
        SELECT @CategoryID = Category_ID 
        FROM tbl_Category 
        WHERE Category_Name = @CategoryName;

        IF @CategoryID IS NULL
        BEGIN
            THROW 50001, 'Category not found in tbl_Category.', 1;
        END

        -- Check for duplicate Category_Name
        IF EXISTS (SELECT 1 FROM tbl_Sub_Category WHERE Sub_Category_Name = @SubCategoryName)
        BEGIN
            THROW 50001, 'SubCategory already exists in tbl_Sub_Category.', 1;
        END

        -- Insert into tbl_Category
        INSERT INTO tbl_Sub_Category (Sub_Category_ID, Sub_Category_Name, Category_ID)
        VALUES (@SubCategoryID, @SubCategoryName, @CategoryID);

        -- Success message
        PRINT 'SubCategory added successfully.';

    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT;
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END

CREATE OR ALTER PROCEDURE InsertType
    @TypeID INT,
    @TypeName NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY

        -- Check for duplicate Type_Name
        IF EXISTS (SELECT 1 FROM tbl_Type WHERE Type_Name = @TypeName)
        BEGIN
            THROW 50001, 'Type already exists in tbl_Type.', 1;
        END

        -- Insert into tbl_Type
        INSERT INTO tbl_Type (Type_ID, Type_Name)
        VALUES (@TypeID, @TypeName);

        -- Success message
        PRINT 'Type added successfully.';

    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT;
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END

SELECT 
    p.Product_ID,
    p.Product_Name,
    (SELECT t.Type_Name 
     FROM tbl_Type t 
     WHERE t.Type_ID = p.Type_ID) AS Type_Name,
    (SELECT c.Category_Name 
     FROM tbl_Category c 
     WHERE c.Category_ID = p.Category_ID) AS Category_Name,
    p.Quantity,
    p.Shelf_Life
FROM 
    tbl_Product p;


CREATE NONCLUSTERED INDEX idx_product_name
ON tbl_Product (Product_Name);

CREATE NONCLUSTERED INDEX idx_quantity
ON tbl_Product (Quantity);

CREATE NONCLUSTERED INDEX idx_shelf_life
ON tbl_Product (Shelf_Life);

CREATE NONCLUSTERED INDEX idx_type_name
ON tbl_Type (Type_Name);

CREATE NONCLUSTERED INDEX idx_category_name
ON tbl_Category (Category_Name);


CREATE OR ALTER PROCEDURE SearchProduct
    @SearchField NVARCHAR(255), -- User input for the search term
    @SearchType NVARCHAR(50) -- Column to search ('Product_Name', 'Type_Name', etc.)
AS
BEGIN
    SET NOCOUNT ON;

    -- Validate inputs
    IF @SearchField IS NULL OR LTRIM(RTRIM(@SearchField)) = ''
    BEGIN
        RAISERROR ('Search field cannot be empty.', 16, 1);
        RETURN;
    END;

    IF @SearchType IS NULL OR 
       @SearchType NOT IN ('Product_Name', 'Type_Name', 'Category_Name', 'Subcategory_Name', 'Quantity', 'Shelf_Life')
    BEGIN
        RAISERROR ('Invalid search type. Choose a valid column name.', 16, 1);
        RETURN;
    END;

    -- Create the search parameter with wildcards added
    DECLARE @SearchParam NVARCHAR(255);
    SET @SearchParam = '%' + @SearchField + '%';

    -- Declare a dynamic SQL variable
    DECLARE @SQL NVARCHAR(MAX);

    -- Search for 'Type_Name'
    IF @SearchType = 'Type_Name'
    BEGIN
        SET @SQL = N'
            SELECT 
                p.Product_ID,
                p.Product_Name,
                (SELECT t.Type_Name 
                 FROM tbl_Type t 
                 WHERE t.Type_ID = p.Type_ID) AS Type_Name,
                (SELECT c.Category_Name 
                 FROM tbl_Category c 
                 WHERE c.Category_ID = p.Category_ID) AS Category_Name,
                p.Quantity,
                p.Shelf_Life,
                STUFF((
                    SELECT '','' + s.Sub_Category_Name
                    FROM tbl_Product_And_Sub_Category ps
                    JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
                    WHERE ps.Product_ID = p.Product_ID
                    FOR XML PATH('''')
                ), 1, 1, '''') AS Subcategory_Name
            FROM 
                tbl_Product p
            WHERE 
                (SELECT t.Type_Name 
                 FROM tbl_Type t 
                 WHERE t.Type_ID = p.Type_ID) LIKE @SearchParam';
    END
    -- Search for 'Category_Name'
    ELSE IF @SearchType = 'Category_Name'
    BEGIN
        SET @SQL = N'
            SELECT 
                p.Product_ID,
                p.Product_Name,
                (SELECT t.Type_Name 
                 FROM tbl_Type t 
                 WHERE t.Type_ID = p.Type_ID) AS Type_Name,
                (SELECT c.Category_Name 
                 FROM tbl_Category c 
                 WHERE c.Category_ID = p.Category_ID) AS Category_Name,
                p.Quantity,
                p.Shelf_Life,
                STUFF((
                    SELECT '','' + s.Sub_Category_Name
                    FROM tbl_Product_And_Sub_Category ps
                    JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
                    WHERE ps.Product_ID = p.Product_ID
                    FOR XML PATH('''')
                ), 1, 1, '''') AS Subcategory_Name
            FROM 
                tbl_Product p
            WHERE 
                (SELECT c.Category_Name 
                 FROM tbl_Category c 
                 WHERE c.Category_ID = p.Category_ID) LIKE @SearchParam';
    END
    -- Search for 'Subcategory_Name'
    ELSE IF @SearchType = 'Subcategory_Name'
	BEGIN
		SET @SQL = N'
			SELECT 
				p.Product_ID,
	            p.Product_Name,
		        (SELECT t.Type_Name 
			     FROM tbl_Type t 
				 WHERE t.Type_ID = p.Type_ID) AS Type_Name,
	            (SELECT c.Category_Name 
		         FROM tbl_Category c 
			     WHERE c.Category_ID = p.Category_ID) AS Category_Name,
	            p.Quantity,
		        p.Shelf_Life,
			    STUFF((
				    SELECT '','' + s.Sub_Category_Name
			        FROM tbl_Product_And_Sub_Category ps
		            JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
	                WHERE ps.Product_ID = p.Product_ID
					FOR XML PATH('''')
				), 1, 1, '''') AS Subcategory_Name
			FROM 
		        tbl_Product p
	        JOIN tbl_Product_And_Sub_Category ps ON p.Product_ID = ps.Product_ID
			JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
		    WHERE s.Sub_Category_Name LIKE @SearchParam';
	END

    -- Search for other columns like 'Product_Name', 'Quantity', 'Shelf_Life'
    ELSE
    BEGIN
        SET @SQL = N'
            SELECT 
                p.Product_ID,
                p.Product_Name,
                (SELECT t.Type_Name 
                 FROM tbl_Type t 
                 WHERE t.Type_ID = p.Type_ID) AS Type_Name,
                (SELECT c.Category_Name 
                 FROM tbl_Category c 
                 WHERE c.Category_ID = p.Category_ID) AS Category_Name,
                p.Quantity,
                p.Shelf_Life,
                STUFF((
                    SELECT '','' + s.Sub_Category_Name
                    FROM tbl_Product_And_Sub_Category ps
                    JOIN tbl_Sub_Category s ON s.Sub_Category_ID = ps.Sub_Category_ID
                    WHERE ps.Product_ID = p.Product_ID
                    FOR XML PATH('''')
                ), 1, 1, '''') AS Subcategory_Name
            FROM 
                tbl_Product p
            WHERE 
                p.' + @SearchType + ' LIKE @SearchParam';
    END

    -- Execute the dynamic SQL with parameterization
    EXEC sp_executesql 
        @SQL,
        N'@SearchParam NVARCHAR(255)',  -- Declare the parameter for the LIKE clause
        @SearchParam;  -- Pass the concatenated value of @SearchParam
END;
GO

CREATE OR ALTER PROCEDURE GetProductExpiryDetails
    @SearchQuery NVARCHAR(10)  -- User input in YYYY, YYYY-MM, or YYYY-MM-DD format
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        -- Temporary table to store product expiry details
        CREATE TABLE #ProductExpiry (
            Product_ID INT,
            Product_Name NVARCHAR(255),
            Quantity INT,
            Expiry_Date DATE
        );

        -- Insert product expiry details
        INSERT INTO #ProductExpiry (Product_ID, Product_Name, Quantity, Expiry_Date)
        SELECT 
            p.Product_ID,
            p.Product_Name,
            pap.QuantityPurchased - 
            ISNULL((SELECT SUM(sap.QuantitySaled)
                    FROM tbl_Product_And_Sale sap
                    WHERE sap.Product_ID = pap.Product_ID), 0) AS RemainingQuantity,
            DATEADD(MONTH, p.Shelf_Life, pp.Purchase_Date) AS Expiry_Date
        FROM tbl_Product p
        JOIN tbl_Product_And_Purchase pap ON p.Product_ID = pap.Product_ID
        JOIN tbl_Purchase pp ON pap.Purchase_ID = pp.Purchase_ID
        WHERE pap.QuantityPurchased > 0;

        -- Filter based on user input length and format
        IF LEN(@SearchQuery) = 4  -- If the input is just the year (YYYY)
        BEGIN
            -- Filter by Year and group by Expiry_Date and Product_ID
            SELECT 
                pe.Product_ID,
                pe.Product_Name,
                SUM(pe.Quantity) AS Quantity,
                pe.Expiry_Date
            FROM #ProductExpiry pe
            WHERE YEAR(pe.Expiry_Date) = CAST(@SearchQuery AS INT)
            GROUP BY pe.Product_ID, pe.Product_Name, pe.Expiry_Date
            ORDER BY pe.Expiry_Date, pe.Product_ID;
        END
        ELSE IF LEN(@SearchQuery) = 7  -- If the input is in Year-Month format (YYYY-MM)
        BEGIN
            -- Filter by Year and Month and group by Expiry_Date and Product_ID
            SELECT 
                pe.Product_ID,
                pe.Product_Name,
                SUM(pe.Quantity) AS Quantity,
                pe.Expiry_Date
            FROM #ProductExpiry pe
            WHERE FORMAT(pe.Expiry_Date, 'yyyy-MM') = @SearchQuery
            GROUP BY pe.Product_ID, pe.Product_Name, pe.Expiry_Date
            ORDER BY pe.Expiry_Date, pe.Product_ID;
        END
        ELSE IF LEN(@SearchQuery) = 10  -- If the input is in Year-Month-Day format (YYYY-MM-DD)
        BEGIN
            -- Filter by Year, Month, and Day and group by Expiry_Date and Product_ID
            SELECT 
                pe.Product_ID,
                pe.Product_Name,
                SUM(pe.Quantity) AS Quantity,
                pe.Expiry_Date
            FROM #ProductExpiry pe
            WHERE CONVERT(VARCHAR(10), pe.Expiry_Date, 120) = @SearchQuery  -- Format: YYYY-MM-DD
            GROUP BY pe.Product_ID, pe.Product_Name, pe.Expiry_Date
            ORDER BY pe.Expiry_Date, pe.Product_ID;
        END
        ELSE
        BEGIN
            -- Handle invalid input
            RAISERROR('Invalid input. Please enter a valid year (YYYY), year-month (YYYY-MM), or year-month-day (YYYY-MM-DD).', 16, 1);
        END

        -- Clean up the temporary table
        DROP TABLE #ProductExpiry;
    END TRY
    BEGIN CATCH
        -- Handle errors
        IF OBJECT_ID('tempdb..#ProductExpiry') IS NOT NULL
            DROP TABLE #ProductExpiry;

        -- Rethrow the error
        THROW;
    END CATCH
END;



EXEC GetProductExpiryDetails 2025;

EXEC GetProductExpiryDetails '2026-12';

ALTER TABLE tbl_Product
ADD IsDeleted BIT NOT NULL DEFAULT 0;

------delete procedure
CREATE OR ALTER PROCEDURE sp_DeleteProductByName
    @ProductName NVARCHAR(255)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        DECLARE @ProductID INT;

        -- Get the Product_ID based on Product_Name
        SELECT @ProductID = Product_ID 
        FROM tbl_Product 
        WHERE Product_Name = @ProductName AND IsDeleted = 0;

        -- Check if the product exists
        IF @ProductID IS NULL
        BEGIN
            THROW 50001, 'Product not found or already deleted.', 1;
        END

        -- Mark the product as deleted
        UPDATE tbl_Product
        SET IsDeleted = 1
        WHERE Product_ID = @ProductID;

        PRINT 'Product marked as deleted successfully.';
    END TRY
    BEGIN CATCH
        -- Error handling
        DECLARE @ErrorMessage NVARCHAR(4000), @ErrorSeverity INT, @ErrorState INT;
        SELECT @ErrorMessage = ERROR_MESSAGE(), @ErrorSeverity = ERROR_SEVERITY(), @ErrorState = ERROR_STATE();
        RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;


CREATE PROCEDURE sp_AddShipment
    @ProductName NVARCHAR(255),
    @Quantity INT,
    @Price FLOAT
AS
BEGIN
    SET NOCOUNT ON; -- Prevent extra result sets

    DECLARE @ProductID INT, @PurchaseID INT;

    -- Get Product ID
    SELECT @ProductID = Product_ID 
    FROM tbl_Product 
    WHERE Product_Name = @ProductName;

    IF @ProductID IS NULL
    BEGIN
        RAISERROR ('Product not found', 16, 1);
        RETURN;
    END;

    -- Get Next Purchase ID
    SELECT @PurchaseID = ISNULL(MAX(Purchase_ID), 0) + 1 FROM tbl_Purchase;

    -- Insert into tbl_Purchase if new
    IF NOT EXISTS (SELECT 1 FROM tbl_Purchase WHERE Purchase_ID = @PurchaseID)
    BEGIN
        INSERT INTO tbl_Purchase (Purchase_ID, Purchase_Date)
        VALUES (@PurchaseID, GETDATE());
    END;

    -- Insert into tbl_Product_And_Purchase
    INSERT INTO tbl_Product_And_Purchase 
        (Product_ID, Purchase_ID, QuantityPurchased, Purchasing_Price, Selling_Price)
    VALUES 
        (@ProductID, @PurchaseID, @Quantity, @Price, @Price);

    -- Update Product Quantity
    UPDATE tbl_Product
    SET Quantity = Quantity + @Quantity
    WHERE Product_ID = @ProductID;
END;


CREATE OR ALTER PROCEDURE SearchShipment
    @SearchType NVARCHAR(20),  -- 'Product' or 'Shipment Date'
    @SearchValue NVARCHAR(50) -- Product Name or Date (YYYY, YYYY-MM, or YYYY-MM-DD)
AS
BEGIN
    SET NOCOUNT ON;

    -- Validate SearchType
    IF @SearchType NOT IN ('Product', 'Shipment Date')
    BEGIN
        PRINT 'Invalid SearchType. Use "Product" or "Shipment Date".';
        RETURN;
    END

    -- Handle Product Search
    IF @SearchType = 'Product'
    BEGIN
        -- Validate SearchValue
        IF @SearchValue IS NULL OR LTRIM(RTRIM(@SearchValue)) = ''
        BEGIN
            PRINT 'Error: Product Name cannot be empty.';
            RETURN;
        END

        SELECT 
            p.Purchase_ID,
            (SELECT Purchase_Date FROM tbl_Purchase WHERE Purchase_ID = p.Purchase_ID) AS Purchase_Date,
            (SELECT Product_Name FROM tbl_Product WHERE Product_ID = p.Product_ID) AS Product_Name,
            p.QuantityPurchased,
            p.Purchasing_Price,
            (p.QuantityPurchased * p.Purchasing_Price) AS Total
        FROM tbl_Product_And_Purchase p
        WHERE p.Product_ID IN (
            SELECT Product_ID 
            FROM tbl_Product 
            WHERE Product_Name LIKE '%' + @SearchValue + '%'
        );
    END

    -- Handle Shipment Date Search
    ELSE IF @SearchType = 'Shipment Date'
    BEGIN
        -- Validate SearchValue
        IF @SearchValue IS NULL OR LTRIM(RTRIM(@SearchValue)) = ''
        BEGIN
            PRINT 'Error: Shipment Date cannot be empty.';
            RETURN;
        END

        SELECT 
            p.Purchase_ID,
            (SELECT Purchase_Date FROM tbl_Purchase WHERE Purchase_ID = p.Purchase_ID) AS Purchase_Date,
            (SELECT Product_Name FROM tbl_Product WHERE Product_ID = p.Product_ID) AS Product_Name,
            p.QuantityPurchased,
            p.Purchasing_Price,
            (p.QuantityPurchased * p.Purchasing_Price) AS Total
        FROM tbl_Product_And_Purchase p
        WHERE p.Purchase_ID IN (
            SELECT Purchase_ID 
            FROM tbl_Purchase 
            WHERE Purchase_Date LIKE @SearchValue + '%'
        );
    END
END
GO


CREATE OR ALTER PROCEDURE SearchSale
    @SearchType NVARCHAR(20),  -- 'Product' or 'Sale Date'
    @SearchValue NVARCHAR(50)  -- Product Name or Date (YYYY, YYYY-MM, or YYYY-MM-DD)
AS
BEGIN
    SET NOCOUNT ON;

    -- Validate SearchType
    IF @SearchType NOT IN ('Product', 'Sale Date')
    BEGIN
        PRINT 'Invalid SearchType. Use "Product" or "Sale Date".';
        RETURN;
    END

    -- Handle Product Search
    IF @SearchType = 'Product'
    BEGIN
        -- Validate SearchValue
        IF @SearchValue IS NULL OR LTRIM(RTRIM(@SearchValue)) = ''
        BEGIN
            PRINT 'Error: Product Name cannot be empty.';
            RETURN;
        END

        SELECT 
            ps.Sale_ID,
            (SELECT Sale_Date FROM tbl_Sale WHERE Sale_ID = ps.Sale_ID) AS Sale_Date,
            (SELECT Product_Name FROM tbl_Product WHERE Product_ID = ps.Product_ID) AS Product_Name,
            ps.QuantitySaled AS Quantity_Sold,
            ps.Sale_Price,
            (ps.QuantitySaled * ps.Sale_Price) AS Total
        FROM tbl_Product_And_Sale ps
        WHERE ps.Product_ID IN (
            SELECT Product_ID 
            FROM tbl_Product 
            WHERE Product_Name LIKE '%' + @SearchValue + '%'
        );
    END

    -- Handle Sale Date Search
    ELSE IF @SearchType = 'Sale Date'
    BEGIN
        -- Validate SearchValue
        IF @SearchValue IS NULL OR LTRIM(RTRIM(@SearchValue)) = ''
        BEGIN
            PRINT 'Error: Sale Date cannot be empty.';
            RETURN;
        END

        SELECT 
            ps.Sale_ID,
            (SELECT Sale_Date FROM tbl_Sale WHERE Sale_ID = ps.Sale_ID) AS Sale_Date,
            (SELECT Product_Name FROM tbl_Product WHERE Product_ID = ps.Product_ID) AS Product_Name,
            ps.QuantitySaled AS Quantity_Sold,
            ps.Sale_Price,
            (ps.QuantitySaled * ps.Sale_Price) AS Total
        FROM tbl_Product_And_Sale ps
        WHERE ps.Sale_ID IN (
            SELECT Sale_ID 
            FROM tbl_Sale 
            WHERE Sale_Date LIKE @SearchValue + '%'
        );
    END
END
GO

CREATE OR ALTER PROCEDURE Calculate_Profit_Statistics 
    @selected_year INT
AS
BEGIN
	SET NOCOUNT ON;
    -- Temporary table to store monthly profit data
    CREATE TABLE #MonthlyProfit (
        Product_ID INT,
        Month INT,
        Profit DECIMAL(10, 2)
    );

    -- Calculate the profit by product and month
    INSERT INTO #MonthlyProfit (Product_ID, Month, Profit)
    SELECT 
        p.Product_ID,
        MONTH(s.Purchase_Date) AS Sale_Month,
        SUM((ps.QuantitySaled * ps.Sale_Price) - (pp.QuantityPurchased * pp.Purchasing_Price)) AS Profit
    FROM tbl_Product p
    LEFT JOIN tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
    LEFT JOIN tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
    LEFT JOIN tbl_Purchase s ON pp.Purchase_ID = s.Purchase_ID
    LEFT JOIN tbl_Sale sp ON ps.Sale_ID = sp.Sale_ID
    WHERE YEAR(s.Purchase_Date) = @selected_year
    GROUP BY p.Product_ID, MONTH(s.Purchase_Date);

    -- Prepare the monthly profit data for the graph (sorted by month)
    SELECT Product_ID, Month, SUM(Profit) AS Monthly_Profit
    FROM #MonthlyProfit
    GROUP BY Product_ID, Month
    ORDER BY Product_ID, Month;

    -- Prepare the product-wise profit for the table (sorted by product)
    SELECT 
        p.Product_Name, 
        SUM((ps.QuantitySaled * ps.Sale_Price) - (pp.QuantityPurchased * pp.Purchasing_Price)) AS Profit
    FROM tbl_Product p
    LEFT JOIN tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
    LEFT JOIN tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
    LEFT JOIN tbl_Purchase s ON pp.Purchase_ID = s.Purchase_ID
    LEFT JOIN tbl_Sale sp ON ps.Sale_ID = sp.Sale_ID
    WHERE YEAR(s.Purchase_Date) = @selected_year
    GROUP BY p.Product_Name
    ORDER BY p.Product_Name;

    -- Clean up temporary table
    DROP TABLE IF EXISTS #MonthlyProfit;
END;



CREATE OR ALTER PROCEDURE GetProductStatisticsByYearMonth
    @Year INT,
    @Month INT
AS
BEGIN
	SET NOCOUNT ON;
    SELECT 
        p.Product_Name,
        SUM(pp.QuantityPurchased) AS Total_Purchase_Quantity,
        SUM(ps.QuantitySaled) AS Total_Sale_Quantity,
        SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Total_Purchase_Amount,
        SUM(ps.QuantitySaled * ps.Sale_Price) AS Total_Sale_Amount,
        SUM(ps.QuantitySaled * ps.Sale_Price) - SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Profit
    FROM 
        tbl_Product p
    JOIN 
        tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
    JOIN 
        tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
    JOIN 
        tbl_Purchase pu ON pu.Purchase_ID = pp.Purchase_ID
    JOIN 
        tbl_Sale sa ON sa.Sale_ID = ps.Sale_ID
    WHERE 
        YEAR(pu.Purchase_Date) = @Year 
        AND MONTH(pu.Purchase_Date) = @Month
        AND YEAR(sa.Sale_Date) = @Year
        AND MONTH(sa.Sale_Date) = @Month
    GROUP BY 
        p.Product_Name;
END


CREATE OR ALTER PROCEDURE GetProductStatisticsByDateRange
    @Year INT,
    @MinDate DATE,
    @MaxDate DATE
AS
BEGIN
	SET NOCOUNT ON;
    SELECT 
        p.Product_Name,
        SUM(pp.QuantityPurchased) AS Total_Purchase_Quantity,
        SUM(ps.QuantitySaled) AS Total_Sale_Quantity,
        SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Total_Purchase_Amount,
        SUM(ps.QuantitySaled * ps.Sale_Price) AS Total_Sale_Amount,
        SUM(ps.QuantitySaled * ps.Sale_Price) - SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Profit
    FROM 
        tbl_Product p
    JOIN 
        tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
    JOIN 
        tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
    JOIN 
        tbl_Purchase pu ON pu.Purchase_ID = pp.Purchase_ID
    JOIN 
        tbl_Sale sa ON sa.Sale_ID = ps.Sale_ID
    WHERE 
        pu.Purchase_Date BETWEEN @MinDate AND @MaxDate
        AND sa.Sale_Date BETWEEN @MinDate AND @MaxDate
    GROUP BY 
        p.Product_Name;
END



EXEC GetProductStatisticsByYear 2024

EXEC GetProductStatisticsByYearMonth 2024,07


CREATE OR ALTER PROCEDURE GetGraphData
    @Year INT,
    @Month INT = NULL,
    @MinDate DATE = NULL,
    @MaxDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold the graph data
    CREATE TABLE #GraphData (
        Period NVARCHAR(20), -- Month/Day depending on the case
        Total_Purchase_Amount FLOAT,
        Total_Sale_Amount FLOAT,
        Total_Profit FLOAT
    );

    -- Logic for Yearly Data (group by months)
    IF @Month IS NULL AND @MinDate IS NULL AND @MaxDate IS NULL
    BEGIN
        DECLARE @MonthNameYearly NVARCHAR(20);
        DECLARE @PurchaseAmountYearly FLOAT;
        DECLARE @SaleAmountYearly FLOAT;

        -- Loop through all months of the year
        DECLARE @MonthNumYearly INT = 1;
        WHILE @MonthNumYearly <= 12
        BEGIN
            -- Get the month name
            SET @MonthNameYearly = DATENAME(MONTH, DATEFROMPARTS(@Year, @MonthNumYearly, 1));

            -- Calculate total purchase amount for the month
            SET @PurchaseAmountYearly = (
                SELECT SUM(pp.QuantityPurchased * pp.Purchasing_Price)
                FROM tbl_Product_And_Purchase pp, tbl_Purchase p
                WHERE pp.Purchase_ID = p.Purchase_ID
                  AND YEAR(p.Purchase_Date) = @Year
                  AND MONTH(p.Purchase_Date) = @MonthNumYearly
            );

            -- Calculate total sale amount for the month
            SET @SaleAmountYearly = (
                SELECT SUM(ps.QuantitySaled * ps.Sale_Price)
                FROM tbl_Product_And_Sale ps, tbl_Sale s
                WHERE ps.Sale_ID = s.Sale_ID
                  AND YEAR(s.Sale_Date) = @Year
                  AND MONTH(s.Sale_Date) = @MonthNumYearly
            );

            -- Insert into #GraphData
            INSERT INTO #GraphData (Period, Total_Purchase_Amount, Total_Sale_Amount, Total_Profit)
            VALUES (
                @MonthNameYearly,
                ISNULL(@PurchaseAmountYearly, 0),
                ISNULL(@SaleAmountYearly, 0),
                ISNULL(@SaleAmountYearly, 0) - ISNULL(@PurchaseAmountYearly, 0)
            );

            -- Move to the next month
            SET @MonthNumYearly = @MonthNumYearly + 1;
        END;
    END

    -- Logic for Monthly Data (group by days)
    ELSE IF @Month IS NOT NULL AND @MinDate IS NULL AND @MaxDate IS NULL
    BEGIN
        DECLARE @DayNumMonthly INT = 1;
        DECLARE @DaysInMonthMonthly INT = DAY(EOMONTH(DATEFROMPARTS(@Year, @Month, 1)));
        DECLARE @PurchaseAmountDaily FLOAT;
        DECLARE @SaleAmountDaily FLOAT;

        -- Loop through all days of the month
        WHILE @DayNumMonthly <= @DaysInMonthMonthly
        BEGIN
            -- Calculate total purchase amount for the day
            SET @PurchaseAmountDaily = (
                SELECT SUM(pp.QuantityPurchased * pp.Purchasing_Price)
                FROM tbl_Product_And_Purchase pp, tbl_Purchase p
                WHERE pp.Purchase_ID = p.Purchase_ID
                  AND YEAR(p.Purchase_Date) = @Year
                  AND MONTH(p.Purchase_Date) = @Month
                  AND DAY(p.Purchase_Date) = @DayNumMonthly
            );

            -- Calculate total sale amount for the day
            SET @SaleAmountDaily = (
                SELECT SUM(ps.QuantitySaled * ps.Sale_Price)
                FROM tbl_Product_And_Sale ps, tbl_Sale s
                WHERE ps.Sale_ID = s.Sale_ID
                  AND YEAR(s.Sale_Date) = @Year
                  AND MONTH(s.Sale_Date) = @Month
                  AND DAY(s.Sale_Date) = @DayNumMonthly
            );

            -- Insert into #GraphData
            INSERT INTO #GraphData (Period, Total_Purchase_Amount, Total_Sale_Amount, Total_Profit)
            VALUES (
                CAST(@DayNumMonthly AS NVARCHAR(20)),
                ISNULL(@PurchaseAmountDaily, 0),
                ISNULL(@SaleAmountDaily, 0),
                ISNULL(@SaleAmountDaily, 0) - ISNULL(@PurchaseAmountDaily, 0)
            );

            -- Move to the next day
            SET @DayNumMonthly = @DayNumMonthly + 1;
        END;
    END

    -- Logic for Date Range
    ELSE IF @MinDate IS NOT NULL AND @MaxDate IS NOT NULL
    BEGIN
        DECLARE @CurrentDateRange DATE = @MinDate;
        DECLARE @PurchaseAmountRange FLOAT;
        DECLARE @SaleAmountRange FLOAT;

        -- Loop through each month in the range
        WHILE @CurrentDateRange <= @MaxDate
        BEGIN
            DECLARE @CurrentYearRange INT = YEAR(@CurrentDateRange);
            DECLARE @CurrentMonthRange INT = MONTH(@CurrentDateRange);
            DECLARE @MonthNameRange NVARCHAR(20) = DATENAME(MONTH, @CurrentDateRange);

            -- Calculate total purchase amount for the month
            SET @PurchaseAmountRange = (
                SELECT SUM(pp.QuantityPurchased * pp.Purchasing_Price)
                FROM tbl_Product_And_Purchase pp, tbl_Purchase p
                WHERE pp.Purchase_ID = p.Purchase_ID
                  AND YEAR(p.Purchase_Date) = @CurrentYearRange
                  AND MONTH(p.Purchase_Date) = @CurrentMonthRange
            );

            -- Calculate total sale amount for the month
            SET @SaleAmountRange = (
                SELECT SUM(ps.QuantitySaled * ps.Sale_Price)
                FROM tbl_Product_And_Sale ps, tbl_Sale s
                WHERE ps.Sale_ID = s.Sale_ID
                  AND YEAR(s.Sale_Date) = @CurrentYearRange
                  AND MONTH(s.Sale_Date) = @CurrentMonthRange
            );

            -- Insert into #GraphData
            INSERT INTO #GraphData (Period, Total_Purchase_Amount, Total_Sale_Amount, Total_Profit)
            VALUES (
                @MonthNameRange + ' ' + CAST(@CurrentYearRange AS NVARCHAR),
                ISNULL(@PurchaseAmountRange, 0),
                ISNULL(@SaleAmountRange, 0),
                ISNULL(@SaleAmountRange, 0) - ISNULL(@PurchaseAmountRange, 0)
            );

            -- Move to the next month
            SET @CurrentDateRange = DATEADD(MONTH, 1, @CurrentDateRange);
        END;
    END

    -- Return the result
    SELECT * FROM #GraphData;

    -- Clean up
    DROP TABLE #GraphData;
END;
GO







CREATE PROCEDURE GetStatisticsData
    @Year INT,
    @Month INT = NULL,
    @MinDate DATE = NULL,
    @MaxDate DATE = NULL
AS
BEGIN
    SET NOCOUNT ON;

    -- Temporary table to hold the statistics data
    CREATE TABLE #StatisticsData (
        Product_Name VARCHAR(50),
        Total_Purchase_Amount FLOAT,
        Total_Sale_Amount FLOAT,
        Profit FLOAT
    );

    -- If a specific month is provided
    IF @Month IS NOT NULL
    BEGIN
        INSERT INTO #StatisticsData
        SELECT
            p.Product_Name,
            SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Total_Purchase_Amount,
            SUM(ps.QuantitySaled * ps.Sale_Price) AS Total_Sale_Amount,
            SUM((ps.QuantitySaled * ps.Sale_Price) - (pp.QuantityPurchased * pp.Purchasing_Price)) AS Profit
        FROM
            tbl_Product p
        INNER JOIN tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
        INNER JOIN tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
        INNER JOIN tbl_Purchase pur ON pp.Purchase_ID = pur.Purchase_ID
        INNER JOIN tbl_Sale sale ON ps.Sale_ID = sale.Sale_ID
        WHERE
            YEAR(pur.Purchase_Date) = @Year
            AND MONTH(pur.Purchase_Date) = @Month
            AND YEAR(sale.Sale_Date) = @Year
            AND MONTH(sale.Sale_Date) = @Month
        GROUP BY
            p.Product_Name;
    END
    -- If a date range is provided
    ELSE IF @MinDate IS NOT NULL AND @MaxDate IS NOT NULL
    BEGIN
        INSERT INTO #StatisticsData
        SELECT
            p.Product_Name,
            SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Total_Purchase_Amount,
            SUM(ps.QuantitySaled * ps.Sale_Price) AS Total_Sale_Amount,
            SUM((ps.QuantitySaled * ps.Sale_Price) - (pp.QuantityPurchased * pp.Purchasing_Price)) AS Profit
        FROM
            tbl_Product p
        INNER JOIN tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
        INNER JOIN tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
        INNER JOIN tbl_Purchase pur ON pp.Purchase_ID = pur.Purchase_ID
        INNER JOIN tbl_Sale sale ON ps.Sale_ID = sale.Sale_ID
        WHERE
            pur.Purchase_Date BETWEEN @MinDate AND @MaxDate
            AND sale.Sale_Date BETWEEN @MinDate AND @MaxDate
        GROUP BY
            p.Product_Name;
    END
    -- If only the year is provided
    ELSE
    BEGIN
        INSERT INTO #StatisticsData
        SELECT
            p.Product_Name,
            SUM(pp.QuantityPurchased * pp.Purchasing_Price) AS Total_Purchase_Amount,
            SUM(ps.QuantitySaled * ps.Sale_Price) AS Total_Sale_Amount,
            SUM((ps.QuantitySaled * ps.Sale_Price) - (pp.QuantityPurchased * pp.Purchasing_Price)) AS Profit
        FROM
            tbl_Product p
        INNER JOIN tbl_Product_And_Purchase pp ON p.Product_ID = pp.Product_ID
        INNER JOIN tbl_Product_And_Sale ps ON p.Product_ID = ps.Product_ID
        INNER JOIN tbl_Purchase pur ON pp.Purchase_ID = pur.Purchase_ID
        INNER JOIN tbl_Sale sale ON ps.Sale_ID = sale.Sale_ID
        WHERE
            YEAR(pur.Purchase_Date) = @Year
            AND YEAR(sale.Sale_Date) = @Year
        GROUP BY
            p.Product_Name;
    END

    -- Return the data
    SELECT * FROM #StatisticsData;

    -- Clean up the temporary table
    DROP TABLE #StatisticsData;
END;


r

SELECT * 
FROM tbl_Product_And_Purchase 
WHERE MONTH(Purchase_ID) = 12 AND YEAR(Purchase_ID) = 2024;

SELECT * 
FROM tbl_Product_And_Sale 
WHERE MONTH(Sale_ID) = 12 AND YEAR(Sale_ID) = 2024;


CREATE OR ALTER TRIGGER trg_InsertPriceHistory
ON tbl_Product
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Insert the updated price into the price history table
    INSERT INTO tbl_pricehistory (Product_ID, Updation_Date, Updated_Price)
    SELECT 
        inserted.Product_ID,
        GETDATE() AS Updation_Date,
        inserted.Price AS Updated_Price
    FROM 
        inserted
    INNER JOIN deleted 
        ON inserted.Product_ID = deleted.Product_ID
    WHERE 
        inserted.Price <> deleted.Price; -- Only log if the price has changed
END;
GO

CREATE TRIGGER trg_insert_pricehistory
ON tbl_Product
AFTER INSERT
AS
BEGIN
    -- Insert the new product's price into tbl_pricehistory
    DECLARE @ProductID INT;
    DECLARE @Price FLOAT;
    DECLARE @UpdationDate DATE;

    -- Get the inserted product's ID and price from the inserted row
    SELECT @ProductID = Product_ID, @Price = Price FROM inserted;
    SET @UpdationDate = GETDATE();  -- Set the current date as the updation date

    -- Insert into price history
    INSERT INTO tbl_pricehistory (Product_ID, Updation_Date, Updated_Price)
    VALUES (@ProductID, @UpdationDate, @Price);
END;

CREATE OR ALTER PROCEDURE UpdateProductDetails
    @ProductName NVARCHAR(255),
    @Price DECIMAL(18, 2) = NULL,
    @ShelfLife DECIMAL(18, 2) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE tbl_Product
    SET 
        Price = COALESCE(@Price, Price),
        Shelf_Life = COALESCE(@ShelfLife, Shelf_Life)
    WHERE 
        Product_Name = @ProductName;

    -- Optionally, return a status message or handle cases where no rows are affected
END;
GO

INSERT INTO tbl_Category (Category_ID, Category_Name, Type_ID) VALUES
(5, 'Fruit Seeds', 1),
(6, 'Tree Seeds', 1),
(7, 'Shrubs', 2),
(8, 'Hanging Plants', 2),
(9, 'Gardening Tools', 3),
(10, 'Compost Fertilizers', 4);
INSERT INTO tbl_Sub_Category (Sub_Category_ID, Sub_Category_Name, Category_ID) VALUES
(5, 'Citrus Fruits', 5),
(6, 'Tropical Fruits', 5),
(7, 'Evergreen Trees', 6),
(8, 'Deciduous Trees', 6),
(9, 'Climbing Shrubs', 7),
(10, 'Flowering Shrubs', 7);
INSERT INTO tbl_Purchase (Purchase_ID, Purchase_Date) VALUES
(10, '2024-10-05'),
(11, '2024-11-12'),
(12, '2023-05-20'),
(13, '2024-08-25'),
(14, '2023-04-10');
select * from tbl_Product_And_Purchase
select * from tbl_Purchase
INSERT INTO tbl_Product_And_Purchase (Product_ID, Purchase_ID, QuantityPurchased, Purchasing_Price, Selling_Price) VALUES
(5, 10, 200, 15.00, 20.00), -- Organic Fertilizer (2024 Purchase)
(1, 11, 50, 1.50, 2.50), -- Tomato Seeds (2024 Purchase)
(2, 12, 30, 120.00, 150.00), -- Rose Plant (2023 Purchase)
(3, 13, 25, 70.00, 75.00), -- Pruning Shears (2024 Purchase)
(4, 14, 120, 18.00, 25.00); -- Urea Fertilizer (2023 Purchase)
INSERT INTO tbl_Sale (Sale_ID, Sale_Date) VALUES
(15, '2024-10-10'), -- Sale for Organic Fertilizer
(16, '2024-11-15'), -- Sale for Tomato Seeds
(17, '2023-05-25'), -- Sale for Rose Plant
(18, '2024-08-30'), -- Sale for Pruning Shears
(19, '2023-04-15'); -- Sale for Urea Fertilizer
select * from tbl_Sale
INSERT INTO tbl_Product_And_Sale (Product_ID, Sale_ID, QuantitySaled, Sale_Price) VALUES
(5, 15, 50, 20.00), -- Organic Fertilizer (Sold 50 out of 200)
(1, 16, 20, 2.50), -- Tomato Seeds (Sold 20 out of 50)
(2, 17, 10, 150.00), -- Rose Plant (Sold 10 out of 30)
(3, 18, 15, 75.00), -- Pruning Shears (Sold 15 out of 25)
(4,19, 80, 25.00); -- Urea Fertilizer (Sold 80 out of 120)

delete from tbl_Product where Product_ID = 8