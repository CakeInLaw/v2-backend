import asyncio
from uuid import uuid4

from sqlalchemy import select, Column
from sqlalchemy.orm import joinedload

from core.db.connection import get_session
from core.db.models import get_base_metadata
from core.schema import create_default_app_schema, get_default_app_schema


async def test():
    from directories.users.models import User
    from directories.employees.models import Employee
    x = get_session()
    session = await anext(x)
    query = select(Employee).options(joinedload(Employee.user)).where(Column("users_1.username", quote=False) == 'ass')
    print(await session.scalars(query))


get_base_metadata(init_first=True)
asyncio.run(test())
