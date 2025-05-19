import pytest
from tests.conftest import ModelForTest
from unittest.mock import AsyncMock
from backend.core.exceptions import MedServiceException
from backend.schemas.base import Schema

class SchemaTest(Schema):
        id: int | None = None
        name: str | None = None

@pytest.mark.asyncio
async def test_success_get(mock_repo, mock_service):
    mock_repo.get_by_id.side_effect = AsyncMock(return_value= ModelForTest(id=1, name="test"))
    result = await mock_service.get_by_id(1)
    assert isinstance(result, ModelForTest)
    assert result.id == 1
    assert result.name == "test"

@pytest.mark.asyncio
async def test_fail_get(mock_repo, mock_service):
    mock_repo.get_by_id.return_value = None
    
    with pytest.raises(MedServiceException):
        await mock_service.get_by_id(1)
    
@pytest.mark.asyncio
async def test_create(mock_repo, mock_service):
    payload = SchemaTest(id=1, name="test")
    mock_repo.create.side_effect = lambda p: ModelForTest(**p)
    result = await mock_service.create(payload)
    assert isinstance(result, ModelForTest)
    assert result.id == 1
    assert result.name == "test"

@pytest.mark.asyncio
async def test_update(mock_repo,mock_service):
    payload = SchemaTest(name="new_test_name")
    instance = ModelForTest(id=1, name="test")

    mock_repo.get_by_id.return_value = instance

    def effect(i, p):
        for key, val in p.items():
            setattr(i, key, val)
        return i
    mock_repo.update.side_effect = effect

    result = await mock_service.patch(1, payload)
    assert isinstance(result, ModelForTest)
    assert result.id == 1
    assert result.name == "new_test_name"

@pytest.mark.asyncio
async def test_delete(mock_repo, mock_service):
    instance = ModelForTest(id=1, name="test")
    mock_repo.get_by_id.return_value = instance
    mock_repo.delete.return_value = instance
    result = await mock_service.delete(1)
    assert result == instance