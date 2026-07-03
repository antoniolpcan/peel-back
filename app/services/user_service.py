from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def create_user(self, user_in: UserCreate) -> User:
        if self.user_repo.get_by_email(email=user_in.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O email já está cadastrado no sistema."
            )
        return self.user_repo.create(user_in=user_in)

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.user_repo.get_all(skip=skip, limit=limit)

    def get_user(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Usuário não encontrado."
            )
        return user

    def update_user(self, user_id: int, user_in: UserUpdate) -> User:
        user = self.get_user(user_id) 
        return self.user_repo.update(db_user=user, user_in=user_in)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.user_repo.delete(db_user=user)