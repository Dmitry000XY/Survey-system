from sqlalchemy import select, update
from src.models.users import User
from src.schemas.users import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def create_user(self, user: UserCreate):
        new_user = User(
            user_id=user.user_id,
            login=user.login,
            password=user.password
        )
        self.session.add(new_user)
        await self.session.flush()
        return new_user

    async def get_all_users(self):
        query = select(User)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_user(self, user_id: int):
        return await self.session.get(User, user_id)

    async def update_user(self, user_id: int, new_data: UserUpdate):
        query = (
            update(User)
            .where(User.user_id == user_id)
            .values(
                login=new_data.login,
                password=new_data.password
            )
            .returning(User)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        if user:
            await self.session.delete(user)
