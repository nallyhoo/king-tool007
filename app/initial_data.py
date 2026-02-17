
import asyncio

from app.core.database import SessionLocal
from app.services.user_service import get_user_by_email, create_user
from app.schemas.user import UserCreate


async def main() -> None:
    print("Creating initial data")
    db = SessionLocal()
    user = await get_user_by_email(db, email="admin@example.com")
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            password="password",
            full_name="Admin",
            is_superuser=True,
        )
        user = await create_user(db, obj_in=user_in)
        print("Superuser created")
    else:
        print("Superuser already exists")
    await db.close()
    print("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
