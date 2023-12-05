from pydantic import BaseModel


__all__ = ["DBConf"]


class DBConf(BaseModel):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: str
    NAME: str

    ECHO: bool = False

    @property
    def connection_url(self) -> str:
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}'
