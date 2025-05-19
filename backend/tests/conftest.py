from unittest.mock import AsyncMock, MagicMock
from backend.repositories.base import SQLCRUDRepository
from backend.services.base import CRUDService
from sqlalchemy.ext.asyncio import AsyncSession
import pytest


class ModelForTest:
    id = 1
    name = "test"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture(scope="function")
def mock_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture(scope="function")
def repo(mock_session):
    repo = SQLCRUDRepository[ModelForTest, int](session=mock_session)
    repo.model = ModelForTest
    return repo

@pytest.fixture(scope="function")
def mock_repo(repo):
    return MagicMock(spec=repo)

@pytest.fixture(scope="function")
def mock_service(mock_repo):
    return CRUDService[ModelForTest, int](mock_repo)

