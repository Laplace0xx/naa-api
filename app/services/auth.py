from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User, Gender, UserRole
from app.repositories.user import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def create_account(self, f_name: str, l_name: str, gender: str, email: str,
                       phone_number: str, dob: str, password: str) -> User:
        if self.user_repo.get_by_email(email):
            raise ValueError("Email already registered")
        if self.user_repo.get_by_phone(phone_number):
            raise ValueError("Phone number already registered")

        hashed_password = pwd_context.hash(password)
        user = User(
            f_name=f_name,
            l_name=l_name,
            gender=Gender(gender),
            email=email,
            phone_number=phone_number,
            dob=dob,
            role=UserRole.AUCTIONEER,
            password_hash=hashed_password
        )
        return self.user_repo.create(user)

    def authenticate(self, email: str | None, phone_number: str | None, password: str) -> User | None:
        if email:
            user = self.user_repo.get_by_email(email)
        elif phone_number:
            user = self.user_repo.get_by_phone(phone_number)
        else:
            return None

        if not user or not pwd_context.verify(password, user.password_hash):
            return None
        return user

    def create_access_token(self, user: User) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {"sub": str(user.id), "exp": expire}
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def reset_password(self, email: str, new_password: str) -> bool:
        user = self.user_repo.get_by_email(email)
        if not user:
            return False
        user.password_hash = pwd_context.hash(new_password)
        self.db.commit()
        return True
