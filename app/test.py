import asyncio
import json

from core.db.connection import get_session
from core.db.models import get_base_metadata
from core.validators.exceptions import ObjectErrors


get_base_metadata(init_first=True)


async def test():
    from directories.employees.repository import EmployeeRepository
    from directories.users.repository import UserRepository
    x = get_session()
    session = await anext(x)
    repo = EmployeeRepository(session)
    repo.bind_instance(await repo.get('6d967433-0baa-4339-a546-f68559f79a5b'))
    repo.current_instance.orig_password = 'adasdasd'
    print(repo.current_instance.__dict__)
    # try:
    #     await UserRepository(session=session).create({"username": "tascar44"})
    # except ObjectErrors as e:
    #     print(json.dumps(e.export(), indent=4))
    #     raise e
    # try:
    #     await repo.update({"name": 'Александр', 'user': 'ab5e9ae4-a784-487f-9ccf-6201d8abb4e8'})
    # except ObjectErrors as e:
    #     print(json.dumps(e.export(), indent=4))
    #     raise e
    # await session.commit()


asyncio.run(test())
