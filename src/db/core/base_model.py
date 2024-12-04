# import logging
# logging.getLogger(__name__).info(f'importing module { __name__}')


from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    def __repr__(self):
        data = [f'{key}: {value}' for key, value in self.__dict__.items() if not key.startswith('_')]
        return f"<{self.__class__.__name__} {', '.join(data)}>"  

class DefaultCols:
    intpk = Annotated[int, mapped_column(primary_key=True)]