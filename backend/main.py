import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv
load_dotenv()

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool

# Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/lostlinked")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Database connection pool
connection_pool = None

# FastAPI app
app = FastAPI(title="LostLinked API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: Optional[int] = None
    username: str
    role: Optional[str] = "user"

class UserInDB(User):
    password: str

class LostItem(BaseModel):
    lost_id: Optional[int] = None
    item_name: str
    description: str
    category: str
    lost_date: str
    location: str
    owner_name: str
    owner_contact: str
    status: Optional[str] = "active"

class FoundItem(BaseModel):
    found_id: Optional[int] = None
    item_name: str
    description: str
    category: str
    found_date: str
    location: str
    finder_name: str
    finder_contact: str
    status: Optional[str] = "active"

# Database helper functions
def get_db_connection():
    """Get a connection from the pool"""
    return connection_pool.getconn()

def release_db_connection(conn):
    """Release connection back to the pool"""
    connection_pool.putconn(conn)

def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """Execute a database query"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            conn.commit()
            if cursor.description:
                result = cursor.fetchone()
                cursor.close()
                return result
            cursor.close()
            return None
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        release_db_connection(conn)

# Authentication functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    """Get a user from the database"""
    query = "SELECT * FROM users WHERE username = %s"
    result = execute_query(query, (username,), fetch=True)
    if result:
        return dict(result[0])
    return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection and create tables"""
    global connection_pool
    
    # Create connection pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        1, 20, DATABASE_URL
    )
    
    # Create tables
    create_tables_query = """
    CREATE TABLE IF NOT EXISTS lost_items (
        lost_id SERIAL PRIMARY KEY,
        item_name VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        lost_date VARCHAR(50),
        location VARCHAR(255),
        owner_name VARCHAR(255),
        owner_contact VARCHAR(255),
        status VARCHAR(50) DEFAULT 'active'
    );
    
    CREATE TABLE IF NOT EXISTS found_items (
        found_id SERIAL PRIMARY KEY,
        item_name VARCHAR(255) NOT NULL,
        description TEXT,
        category VARCHAR(100),
        found_date VARCHAR(50),
        location VARCHAR(255),
        finder_name VARCHAR(255),
        finder_contact VARCHAR(255),
        status VARCHAR(50) DEFAULT 'active'
    );
    
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) DEFAULT 'user'
    );
    """
    
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(create_tables_query)
        conn.commit()
        cursor.close()
        
        # Create default admin user
        admin_password = get_password_hash("admin123")
        check_admin_query = "SELECT * FROM users WHERE username = 'admin'"
        cursor = conn.cursor()
        cursor.execute(check_admin_query)
        if not cursor.fetchone():
            create_admin_query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            cursor.execute(create_admin_query, ("admin", admin_password, "admin"))
            conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Startup error: {e}")
        conn.rollback()
    finally:
        release_db_connection(conn)

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection pool"""
    if connection_pool:
        connection_pool.closeall()

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to LostLinked API"}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint - generates JWT token"""
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/lost-items", response_model=LostItem, status_code=status.HTTP_201_CREATED)
async def create_lost_item(item: LostItem):
    """Create a new lost item"""
    query = """
    INSERT INTO lost_items (item_name, description, category, lost_date, location, owner_name, owner_contact, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING *
    """
    result = execute_query(
        query,
        (item.item_name, item.description, item.category, item.lost_date, 
         item.location, item.owner_name, item.owner_contact, item.status)
    )
    return dict(result)

@app.post("/found-items", response_model=FoundItem, status_code=status.HTTP_201_CREATED)
async def create_found_item(item: FoundItem):
    """Create a new found item"""
    query = """
    INSERT INTO found_items (item_name, description, category, found_date, location, finder_name, finder_contact, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING *
    """
    result = execute_query(
        query,
        (item.item_name, item.description, item.category, item.found_date,
         item.location, item.finder_name, item.finder_contact, item.status)
    )
    return dict(result)

@app.get("/lost-items")
async def get_lost_items():
    """Get all lost items"""
    query = "SELECT * FROM lost_items ORDER BY lost_id DESC"
    result = execute_query(query, fetch=True)
    return [dict(row) for row in result]

@app.get("/found-items")
async def get_found_items():
    """Get all found items"""
    query = "SELECT * FROM found_items ORDER BY found_id DESC"
    result = execute_query(query, fetch=True)
    return [dict(row) for row in result]

@app.delete("/items/{item_type}/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_type: str, item_id: int, current_user: dict = Depends(get_current_user)):
    """Delete an item (protected endpoint)"""
    if item_type not in ["lost", "found"]:
        raise HTTPException(status_code=400, detail="Invalid item type")
    
    table_name = f"{item_type}_items"
    id_column = f"{item_type}_id"
    
    # Check if item exists
    check_query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
    result = execute_query(check_query, (item_id,), fetch=True)
    
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Delete the item
    delete_query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
    execute_query(delete_query, (item_id,))
    
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
