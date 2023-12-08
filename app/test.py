import asyncio
import json

from sqlalchemy import select

from core.db.connection import get_session
from core.db.models import get_base_metadata
from core.repositories import ObjectRepository
from core.validators.exceptions import ObjectErrors
from directories.employees.models import Employee
from directories.users.models import User

get_base_metadata(init_first=True)


class EmployeeRepository(ObjectRepository[Employee]):
    model = Employee


async def test():
    x = get_session()
    session = await anext(x)
    user = await session.scalar(select(User).filter(User.id == 'ab5e9ae4-a784-487f-9ccf-6201d8abb4e8'))
    print(user.username)
    user.username = 'tascan44'
    print(user.username)
    try:
        await EmployeeRepository.validator.validate({"name": "aa"*1000}, EmployeeRepository(session))
    except ObjectErrors as e:
        print(json.dumps(e.export(), indent=4))
        raise e
    await session.commit()


asyncio.run(test())
