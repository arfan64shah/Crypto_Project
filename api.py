from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
from typing import List

app = FastAPI(title="Cryptocurrency API", description="API for accessing cryptocurrency data")

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': '(Holacheramba48)',  # Replace with your MySQL password
    'database': 'crypto_currencies'
}

# Pydantic model for cryptocurrency data
class Crypto(BaseModel):
    id: int
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: int

# Helper function to get database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# API endpoints
@app.get("/cryptocurrencies/", response_model=List[Crypto])
async def get_cryptocurrencies():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM cryptocurrencies")
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return results
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/cryptocurrencies/{crypto_id}", response_model=Crypto)
async def get_crypto_by_id(crypto_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM cryptocurrencies WHERE id = %s", (crypto_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result is None:
            raise HTTPException(status_code=404, detail="Cryptocurrency not found")
        
        return result
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")