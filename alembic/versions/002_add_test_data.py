"""Add test data

Revision ID: 002_test_data
Revises: 001_initial
Create Date: 2026-01-27 12:01:00.000000

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import text
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = '002_test_data'
down_revision: Union[str, None] = '001_initial'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    # Хешируем пароли
    user_password_hash = pwd_context.hash("user123")
    admin_password_hash = pwd_context.hash("admin123")
    
    # Создаем тестового пользователя
    connection = op.get_bind()
    connection.execute(
        text(
            """
            INSERT INTO users (email, hashed_password, full_name, is_active)
            VALUES (:email, :password, :full_name, :is_active)
            """
        ),
        {"email": "user@test.com", "password": user_password_hash, "full_name": "Test User", "is_active": True}
    )
    
    # Создаем счет для тестового пользователя (user_id = 1)
    connection.execute(
        text(
            """
            INSERT INTO accounts (user_id, balance)
            VALUES (:user_id, :balance)
            """
        ),
        {"user_id": 1, "balance": 0.00}
    )
    
    # Создаем тестового администратора
    connection.execute(
        text(
            """
            INSERT INTO admins (email, hashed_password, full_name, is_active)
            VALUES (:email, :password, :full_name, :is_active)
            """
        ),
        {"email": "admin@test.com", "password": admin_password_hash, "full_name": "Test Admin", "is_active": True}
    )


def downgrade() -> None:
    op.execute("DELETE FROM payments WHERE user_id = 1")
    op.execute("DELETE FROM accounts WHERE user_id = 1")
    op.execute("DELETE FROM users WHERE email = 'user@test.com'")
    op.execute("DELETE FROM admins WHERE email = 'admin@test.com'")
