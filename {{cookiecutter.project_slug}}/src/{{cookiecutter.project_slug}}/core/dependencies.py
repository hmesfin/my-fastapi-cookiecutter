from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from {{ cookiecutter.project_slug }}.db import get_db

DBSession = Annotated[AsyncSession, Depends(get_db)]
