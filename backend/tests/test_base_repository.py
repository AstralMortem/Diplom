import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
import asyncio
from typing import Any, TypeVar, Generic, Optional
from fastapi_pagination import Page, Params
from fastapi import status

# Mock the necessary imports and types
class ICRUDRepository(Generic[TypeVar('M'), TypeVar('ID')]):
    pass

class Filter:
    def filter(self, query):
        pass

class MedServiceException(Exception):
    def __init__(self, status_code, title, detail, debug=None):
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.debug = debug
        super().__init__(f"{title}: {detail}")

# Mock the paginate function
async def paginate(session, query, pagination_params):
    pass

# Import the class to test
from backend.repositories.base import SQLCRUDRepository

# Create a mock model for testing
class MockModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(default=1)
    name: Mapped[str] = mapped_column(default="test")
    
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)
            
    #     super().__init__()

@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session

@pytest.fixture
def crud_repository(mock_async_session):
    repository = SQLCRUDRepository(mock_async_session)
    repository.model = MockModel
    return repository

@pytest.mark.asyncio
async def test_get_by_id(crud_repository, mock_async_session):
    # Arrange
    mock_id = 1
    mock_model_instance = MockModel(id=mock_id)
    mock_async_session.get.return_value = mock_model_instance
    
    # Act
    result = await crud_repository.get_by_id(mock_id)
    
    # Assert
    mock_async_session.get.assert_called_once_with(MockModel, mock_id)
    assert result == mock_model_instance

@pytest.mark.asyncio
async def test_get_by_id_not_found(crud_repository, mock_async_session):
    # Arrange
    mock_id = 999
    mock_async_session.get.return_value = None
    
    # Act
    result = await crud_repository.get_by_id(mock_id)
    
    # Assert
    mock_async_session.get.assert_called_once_with(MockModel, mock_id)
    assert result is None

# @pytest.mark.asyncio
# async def test_get_by_field(crud_repository, mock_async_session):
#     # Arrange
#     field = "name"
#     value = "test"
#     mock_model_instance = MockModel(name=value)
#     mock_async_session.scalar.return_value = mock_model_instance
    
#     # Act
#     result = await crud_repository.get_by_field(field, value)
    
#     # Assert
#     mock_async_session.scalar.assert_called_once()
#     assert result == mock_model_instance

# @pytest.mark.asyncio
# async def test_get_by_field_not_found(crud_repository, mock_async_session):
#     # Arrange
#     field = "name"
#     value = "nonexistent"
#     mock_async_session.scalar.return_value = None
    
#     # Act
#     result = await crud_repository.get_by_field(field, value)
    
#     # Assert
#     mock_async_session.scalar.assert_called_once()
#     assert result is None

@pytest.mark.asyncio
async def test_create(crud_repository, mock_async_session):
    # Arrange
    payload = {"id": 1, "name": "test_create"}
    
    # Act
    result = await crud_repository.create(payload)
    
    # Assert
    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_called_once()
    mock_async_session.refresh.assert_called_once()
    assert result.id == payload["id"]
    assert result.name == payload["name"]

@pytest.mark.asyncio
async def test_update(crud_repository, mock_async_session):
    # Arrange
    instance = MockModel(id=1, name="old_name")
    payload = {"name": "updated_name"}
    
    # Act
    result = await crud_repository.update(instance, payload)
    
    # Assert
    mock_async_session.add.assert_called_once_with(instance)
    mock_async_session.commit.assert_called_once()
    mock_async_session.refresh.assert_called_once_with(instance)
    assert result.name == "updated_name"

@pytest.mark.asyncio
async def test_delete(crud_repository, mock_async_session):
    # Arrange
    instance = MockModel(id=1, name="to_delete")
    
    # Act
    await crud_repository.delete(instance)
    
    # Assert
    mock_async_session.delete.assert_called_once_with(instance)
    mock_async_session.commit.assert_called_once()

# @pytest.mark.asyncio
# async def test_get_all_no_filter(crud_repository, mock_async_session):
#     # Arrange
#     pagination_params = Params(page=1, size=10)
#     expected_result = Page(items=[MockModel(), MockModel()], total=2, page=1, size=10)
    
#     with patch('fastapi_pagination.ext.sqlalchemy.paginate', new_callable=AsyncMock) as mock_paginate:
#         mock_paginate.return_value = expected_result
        
#         # Act
#         result = await crud_repository.get_all(pagination_params)
        
#         # Assert
#         mock_paginate.assert_called_once()
#         assert result == expected_result

# @pytest.mark.asyncio
# async def test_get_all_with_filter_no_joins(crud_repository, mock_async_session):
#     # Arrange
#     pagination_params = Params(page=1, size=10)
#     mock_filter = MagicMock(spec=Filter)
    
#     # Act & Assert
#     with pytest.raises(MedServiceException) as exc_info:
#         await crud_repository.get_all(pagination_params, filter=mock_filter)
    
#     assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
#     assert "Joins are required for filtering" in str(exc_info.value)

# @pytest.mark.asyncio
# async def test_get_all_with_filter_invalid_join(crud_repository, mock_async_session):
#     # Arrange
#     pagination_params = Params(page=1, size=10)
#     mock_filter = MagicMock(spec=Filter)
#     joins = {"invalid_join"}
    
#     # Act & Assert
#     with pytest.raises(MedServiceException) as exc_info:
#         await crud_repository.get_all(pagination_params, filter=mock_filter, joins=joins)
    
#     assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
#     assert "Join method not found" in str(exc_info.value)

# @pytest.mark.asyncio
# async def test_get_all_with_filter_valid_join(crud_repository, mock_async_session):
#     # Arrange
#     pagination_params = Params(page=1, size=10)
#     mock_filter = MagicMock(spec=Filter)
#     joins = {"test"}
#     expected_result = Page(items=[MockModel(), MockModel()], total=2, page=1, size=10)
    
#     # Create a test join method
#     async def _test_join(query, **kwargs):
#         return query
    
#     crud_repository._test_join = _test_join
#     mock_filter.filter.return_value = select(MockModel)
    
#     with patch('fastapi_pagination.ext.sqlalchemy.paginate', new_callable=AsyncMock) as mock_paginate:
#         mock_paginate.return_value = expected_result
        
#         # Act
#         result = await crud_repository.get_all(pagination_params, filter=mock_filter, joins=joins)
        
#         # Assert
#         mock_paginate.assert_called_once()
#         mock_filter.filter.assert_called_once()
#         assert result == expected_result

@pytest.mark.asyncio
async def test_bulk_create(crud_repository, mock_async_session):
    # Arrange
    payloads = [
        {"id": 1, "name": "item1"},
        {"id": 2, "name": "item2"}
    ]
    
    # Act
    result = await crud_repository.bulk_create(payloads)
    
    # Assert
    mock_async_session.add_all.assert_called_once()
    mock_async_session.commit.assert_called_once()
    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].name == "item1"
    assert result[1].id == 2
    assert result[1].name == "item2"

@pytest.mark.asyncio
async def test_bulk_update(crud_repository, mock_async_session):
    # Arrange
    instances = [
        MockModel(id=1, name="old_name1"),
        MockModel(id=2, name="old_name2")
    ]
    payloads = [
        {"name": "updated_name1"},
        {"name": "updated_name2"}
    ]
    
    # Act
    result = await crud_repository.bulk_update(instances, payloads)
    
    # Assert
    mock_async_session.add_all.assert_called_once_with(instances)
    mock_async_session.commit.assert_called_once()
    assert result[0].name == "updated_name1"
    assert result[1].name == "updated_name2"

@pytest.mark.asyncio
async def test_bulk_update_with_different_length_inputs(crud_repository):
    # Arrange
    instances = [
        MockModel(id=1, name="old_name1"),
        MockModel(id=2, name="old_name2")
    ]
    payloads = [
        {"name": "updated_name1"}
    ]
    
    # Act & Assert
    with pytest.raises(IndexError):
        await crud_repository.bulk_update(instances, payloads)