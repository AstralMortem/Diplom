from fastapi_pagination import Page, Params
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .conftest import ModelForTest



# SQLAlchemy mocked select class
class SelectTest:
    def __init__(self, model: ModelForTest):
        self.model = model
    def where(self, *args):
        return self.model


class Filter:
    def filter(self, query):
        pass



@pytest.mark.asyncio
async def test_get_by_pk(repo, mock_session):
    mock_session.get.return_value = ModelForTest(id=1, name="test_item")
    result = await repo.get_by_id(1)
    mock_session.get.assert_called_once_with(ModelForTest, 1)
    assert result.id == 1
    assert result.name == "test_item"
    
@pytest.mark.asyncio
async def test_get_by_field(repo, mock_session):
    model = ModelForTest(id=1, name="test_item")
    with patch("backend.repositories.base.select") as select:
        select.side_effect = SelectTest
        mock_session.scalar.return_value = model
        result = await repo.get_by_field("name", "test_item")
    mock_session.scalar.assert_called_once()
    assert result == model

@pytest.mark.asyncio
async def test_create(repo, mock_session):
    payload = {"id":1, "name": "new_test_item"}
    result = await repo.create(payload)
    assert type(result) == ModelForTest
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.id == 1
    assert result.name == "new_test_item"

@pytest.mark.asyncio
async def test_update(repo, mock_session):
    instance = ModelForTest(id=1, name="old_name")
    payload = {"name": "updated_name"}
    result = await repo.update(instance, payload)

    mock_session.add.assert_called_once_with(instance)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert result.name == "updated_name"

@pytest.mark.asyncio
async def test_delete(repo, mock_session):
    instance = ModelForTest(id=1, name="to_delete")
    await repo.delete(instance)
    mock_session.delete.assert_called_once_with(instance)
    mock_session.commit.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_without_filter(repo, mock_session):
    pagination_params = Params(page=1, size=10)
    expected_page = Page(items=[ModelForTest(id=1), ModelForTest(id=2)], total=2, page=1, size=10)

    with patch('backend.repositories.base.paginate', autospec=True) as mock_paginate:
        with patch("backend.repositories.base.select") as select:
            select.side_effect = SelectTest
            mock_paginate.side_effect = AsyncMock(return_value=expected_page)
            result = await repo.get_all(pagination_params)
            mock_paginate.assert_called_once()
            assert result == expected_page

