import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv




def create_tables():
    connection = psycopg2.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        database=os.getenv('DATABASE'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD')
    )
    cursor = connection.cursor()

    queries = [
        """
        CREATE TABLE IF NOT EXISTS AccountUser (
            user_ID SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Industry (
            industry_ID SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS StockPool (
            stock_ID SERIAL PRIMARY KEY,
            ticker_symbol VARCHAR(50) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            path TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS StockEntry (
            entry_ID SERIAL PRIMARY KEY,
            user_ID INT NOT NULL,
            Industry_ID INT NOT NULL,
            stock VARCHAR(255) NOT NULL,
            number INT NOT NULL,
            date DATE NOT NULL,
            price_per_share DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (user_ID) REFERENCES AccountUser(user_ID) ON DELETE CASCADE,
            FOREIGN KEY (Industry_ID) REFERENCES Industry(industry_ID) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS AISuggestions (
            suggestion_ID SERIAL PRIMARY KEY,
            Industry_ID INT NOT NULL,
            stock_ID INT NOT NULL,
            Rating DECIMAL(3,2) NOT NULL,
            FOREIGN KEY (stock_ID) REFERENCES StockPool(stock_ID) ON DELETE CASCADE,
            FOREIGN KEY (Industry_ID) REFERENCES Industry(industry_ID) ON DELETE CASCADE 
        );
        """
    ]

    for query in queries:
        cursor.execute(query)

    sample_inserts = [
        """
        INSERT INTO AccountUser (first_name, last_name, email, password) VALUES
        ('John', 'Doe', 'john.doe@test.com', '$2b$12$4e/HO.SSfiQYDmOvMNy7d.bTVdMu7R9jVgniotZxzi9iZNjiH1Rze'),
        ('Jane', 'Smith', 'jane.smith@test.com', '$2b$12$4e/HO.SSfiQYDmOvMNy7d.bTVdMu7R9jVgniotZxzi9iZNjiH1Rze');
        """,
        """
        INSERT INTO Industry (name) VALUES
        ('Energy'),
        ('Materials'),
        ('Industrials'),
        ('Consumer Discretionary'),
        ('Consumer Staples'),
        ('Health Care'),
        ('Financials'),
        ('Information Technology'),
        ('Communication Services'),
        ('Utilities'),
        ('Real Estate');
        """,
        """
        INSERT INTO StockPool (ticker_symbol, name, path) VALUES
        ('AAPL', 'Apple Inc.', '/stocks'),
        ('AFL', 'Aflac', '/stocks'),
        ('AMZN', 'Amazon', '/stocks'),
        ('ABNB', 'Airbnb', '/stocks'),
        ('AIG', 'American International Group', '/stocks'),
        ('AMGN', 'Amgen', '/stocks'),
        ('CMG', 'Chipotle Mexican Grill', '/stocks')
        ('MSFT', 'Microsoft Corporation', '/stocks'),
        ('GOOGL', 'Alphabet Inc. (Google)', '/stocks'),
        ('TSLA', 'Tesla Inc.', '/stocks'),
        ('META', 'Meta Platforms Inc.', '/stocks'),
        ('NVDA', 'NVIDIA Corporation', '/stocks'),
        ('JPM', 'JPMorgan Chase & Co.', '/stocks'),
        ('UNH', 'UnitedHealth Group Incorporated', '/stocks'),
        ('XOM', 'Exxon Mobil Corporation', '/stocks'),
        ('V', 'Visa Inc.', '/stocks'),
        ('JNJ', 'Johnson & Johnson', '/stocks'),
        ('PG', 'Procter & Gamble Co.', '/stocks'),                
        ('HD', 'Home Depot Inc.', '/stocks'),                     
        ('MA', 'Mastercard Inc.', '/stocks'),                     
        ('BAC', 'Bank of America Corp.', '/stocks'),              
        ('PFE', 'Pfizer Inc.', '/stocks'),                        
        ('T', 'AT&T Inc.', '/stocks'),                            
        ('BA', 'Boeing Company', '/stocks'),                      
        ('CVX', 'Chevron Corporation', '/stocks'),                
        ('PEP', 'PepsiCo, Inc.', '/stocks'),                      
        ('COST', 'Costco Wholesale Corporation', '/stocks');      
        """,
        """
        INSERT INTO StockEntry (user_ID, Industry_ID, stock, number, date, price_per_share) VALUES
        (1, 8, 'AAPL', 10, '2015-08-22', 150.50),
        (2, 7, 'AFL', 5, '2023-02-03', 120.75),
        (1, 4, 'AMZN', 7, '2017-11-12', 238.50),
        (2, 4, 'ABNB', 12, '2025-01-31', 140.30),
        (1, 7, 'AIG', 6, '2024-06-28', 58.75),
        (2, 6, 'AMGN', 8, '2020-03-01', 315.50),
        (1, 4, 'CMG', 4, '2021-10-05', 52.57);
        """,
        """
        INSERT INTO AISuggestions (suggestion_ID, Industry_ID, stock_ID, Rating) VALUES
        (1, 8, 1, 4.5),      -- AAPL, Information Technology
        (2, 7, 2, 4.0),      -- AFL, Financials
        (3, 4, 3, 4.7),      -- AMZN, Consumer Discretionary
        (4, 4, 4, 4.2),      -- ABNB, Consumer Discretionary
        (5, 7, 5, 3.9),      -- AIG, Financials
        (6, 6, 6, 4.4),      -- AMGN, Health Care
        (7, 4, 7, 4.8),      -- CMG, Consumer Discretionary
        (8, 8, 8, 4.6),      -- MSFT, Information Technology
        (9, 8, 9, 4.7),      -- GOOGL, Information Technology
        (10, 4, 10, 4.4),    -- TSLA, Consumer Discretionary
        (11, 8, 11, 4.5),    -- META, Information Technology
        (12, 8, 12, 4.9),    -- NVDA, Information Technology
        (13, 7, 13, 4.3),    -- JPM, Financials
        (14, 6, 14, 4.2),    -- UNH, Health Care
        (15, 1, 15, 3.8),    -- XOM, Energy
        (16, 7, 16, 4.4),    -- V, Financials
        (17, 6, 17, 4.5),    -- JNJ, Health Care
        (18, 5, 18, 4.3),     -- PG, Consumer Staples
        (19, 4, 19, 4.2),     -- HD, Consumer Discretionary
        (20, 7, 20, 4.6),     -- MA, Financials
        (21, 7, 21, 4.1),     -- BAC, Financials
        (22, 6, 22, 4.0),     -- PFE, Health Care
        (23, 9, 23, 3.9),     -- T, Communication Services
        (24, 3, 24, 4.4),     -- BA, Industrials
        (25, 1, 25, 4.2),     -- CVX, Energy
        (26, 5, 26, 4.5),     -- PEP, Consumer Staples
        (27, 5, 27, 4.7);     -- COST, Consumer Staples
        """
    ]

    for insert in sample_inserts:
        cursor.execute(insert)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    load_dotenv()

    create_tables()
