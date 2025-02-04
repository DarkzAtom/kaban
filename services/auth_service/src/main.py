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


# password-recovery secrets, variables, etc. i will move it later into the .envs, im just lazy for now to do this. thanks
JWT_SECRET_KEY = 'ef0691a0e48bab988adb9faf3fda0b93501e0a7fd363c3fadc7b47b62d1c159d'
JWT_ALGORITHM = 'HS256'

import jwt
from datetime import datetime, timedelta, timezone
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig


email_conf = ConnectionConfig(
    MAIL_USERNAME = "claj.automail@gmail.com",
    MAIL_PASSWORD = "lyay kmcb udwz vrqm",
    MAIL_FROM = "claj.automail@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True
)


@app.post('/auth/password-recovery')
async def password_recovery(user_email: schemas.UserPasswordRecovery, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user_email.email)
    if not db_user:
        logger.error("User not found, recovery mail won't be sent")
        raise HTTPException(status_code=400, detail="User not found")
    token = jwt.encode(
        {
            'email': user_email.email,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=30),
        },
        JWT_SECRET_KEY,
        JWT_ALGORITHM
    )

    # Create the reset link
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    # Prepare email message
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[user_email.email],
        body=f"""
            <html>
                <body>
                    <h2>Password Reset Request</h2>
                    <p>Click the link below to reset your password:</p>
                    <p><a href="{reset_link}">Reset Password</a></p>
                    <p>This link will expire in 30 minutes.</p>
                    <p>If you didn't request this, please ignore this email.</p>
                </body>
            </html>
            """,
        subtype="html"
    )

    # Send email
    fm = FastMail(email_conf)
    try:
        await fm.send_message(message)
        logger.info(f"Password reset email sent to {user_email.email}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")

    return {"message": "Password reset instructions sent to your email"}

@app.post('/auth/postprocess-pswd-recovery')
async def reset_password(data: schemas.UserPasswordRecoveryPostProcessing, db: Session = Depends(database.get_db)):
    try:

        token = data.token
        new_password = data.new_password
        # verifying token mafaka

        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get('email')

        if not email:
            raise HTTPException(status_code=400, detail="Invalid token")


        updated_user = crud.update_user_password(db, email, new_password)
        if not updated_user:
            raise HTTPException(status_code=400, detail="User not found")


        return {"message": f"Password reset successfully for {email}"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Reset link has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid reset token")


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