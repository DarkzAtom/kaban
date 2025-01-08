# auth_service/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, database, crud, schemas
import logging


# logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler("app.log", encoding='utf-8'),  # Write logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

models.Base.metadata.create_all(bind=database.engine)

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/auth/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        error_msg = f'Email already registered: {user.email}'
        logger.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)
    logger.info(f'Successfully registered user: {user.email}')
    return crud.create_user(db=db, user=user)

@app.get('/auth/test-db')
def test_db(db: Session = Depends(get_db)):
    try:
        # testing with the simple query
        result = db.execute(text("SELECT 1")).fetchone()
        if result[0] == 1:
            return {"message": "Database connection successful!"}
        else:
            return {"message": "Unexpected result from the database!"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}


@app.get("/auth/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users



@app.get("/auth/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/auth/login", response_model=schemas.UserOut)
async def login_user(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = crud.login_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return db_user

@app.get('/auth')
async def root():
    return {'root': 'is working'}


# usage through the uvicorn -> uvicorn src.main:app --reload