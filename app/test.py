import asyncio
import json

from core.db.connection import get_session
from core.db.models import get_base_metadata
from core.repositories import DirectoryRepository
from core.validators.exceptions import ObjectErrors
from directories.employees.models import Employee
from directories.users.models import User

get_base_metadata(init_first=True)


class EmployeeRepository(DirectoryRepository[Employee]):
    model = Employee


class UserRepository(DirectoryRepository[User]):
    model = User


async def test():
    x = get_session()
    session = await anext(x)
    repo = EmployeeRepository(session)
    repo.bind_instance(await repo.get('6d967433-0baa-4339-a546-f68559f79a5b'))
    try:
        await repo.update({"name": 'Александр', 'user': 'ab5e9ae4-a784-487f-9ccf-6201d8abb4e8'})
    except ObjectErrors as e:
        print(json.dumps(e.export(), indent=4))
        raise e
    await session.commit()


asyncio.run(test())
