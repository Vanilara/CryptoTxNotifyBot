from db.repositories.groups import GroupsRep
from db.repositories.users import UsersRep
from db.repositories.wallets import WalletsRep
from db.connector import async_session_maker



class UnitOfWork:
    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRep(self.session)
        self.wallets = WalletsRep(self.session)
        self.groups = GroupsRep(self.session)
        
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


    