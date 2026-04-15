from uuid import uuid4
from unittest.mock import AsyncMock
from fastapi import HTTPException
import pytest
from datetime import datetime

from app.service import create_request_service, get_request_by_id_service,get_requests_by_resident_id, get_requests_by_resident_id_service
from app.models import Request
from app.database import StatusEnum
from app.schemas import RequestCreate




fake_request = Request(
    id=uuid4(),
    title="test_title",
    description="test_description",
    resident_id=1,
    building_id=1,
    status=StatusEnum.PENDING,
    created_at=datetime.now(),
    updated_at=datetime.now(),
    assigned_worker=None,
)


fake_schema = RequestCreate(
    title="test_title",
    description="test_description",
    resident_id=1,
    building_id=1,
)


#Проверяем не результат а поведение функции, т.е. проверяем то что она правильно вызывает create_request(), commit(), publish()
#Мы не проверяем что она делает запись в БД или в кафку или делает ли commit()
#Мы проверяем, что все работает как ожидается, поэтому это unit-тест, для этих проверок нужны Моки, чтобы иммиторвать БД, кафку итд. 

# Внутри сервиса происходит три вещи:
#   1.Вызывается create_request (репо, пишет в БД)
#   2.Вызывается db.commit() (фиксирует транзакцию)
#   3.Вызывается publish_request (публикует в Kafka)
# Тест хочет убедиться, что все три шага реально произошли — без реальной БД и без реального Kafka.


@pytest.mark.asyncio
async def test_create_request_service(mocker):
    #mocker - объект, который подменяет реальные вызовы на заглушки, прям во время теста(фикстура)
    
    mock_create = mocker.patch("app.service.create_request", return_value=fake_request) #Мок для вызова create_request в create_request_service
    mock_publish = mocker.patch("app.service.publish_request") #Мок для вызова publish_request в create_request_service

    mock_db = AsyncMock()   #Создали мок базы данных

    await create_request_service(fake_schema, mock_db) # Сам вызов create_request_service, вызовы create_request и publish_request заменены на Мок выше

    mock_create.assert_called_once_with(fake_schema, mock_db)# Проверка что в create_request_service была вызвана функция create_request один раз  
    mock_db.commit.assert_called_once() # Проверка что в create_request_service был коммит и только один
    mock_publish.assert_called_once_with(fake_request) # Проверка что в create_request_service была одна публикация в кафку и что create_request вернул fake_request без изменений 

    
@pytest.mark.asyncio
async def test_get_requests_by_resident_id_service(mocker):
    mock_get = mocker.patch("app.service.get_requests_by_resident_id", return_value=[fake_request])

    mock_db = AsyncMock()

    result = await get_requests_by_resident_id_service(fake_schema.resident_id, mock_db)

    mock_get.assert_called_once_with(fake_schema.resident_id, mock_db)

    assert result == [fake_request]



@pytest.mark.asyncio
async def test_get_requests_by_resident_id_service_not_found(mocker):
    mocker.patch("app.service.get_requests_by_resident_id", return_value=[])

    mock_db = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await get_requests_by_resident_id_service(fake_schema.resident_id, mock_db)
        
    assert exc_info.value.status_code == 404





@pytest.mark.asyncio
async def test_get_request_by_id_service(mocker):

    mock_get = mocker.patch("app.service.get_request_by_id", return_value=fake_request)
    mock_db = AsyncMock()
    request_id = uuid4()
    result = await get_request_by_id_service(request_id, mock_db)
    mock_get.assert_called_once_with(request_id, mock_db)
    assert result == fake_request




@pytest.mark.asyncio
async def test_get_request_by_id_service_with_none(mocker):

    mock_get = mocker.patch("app.service.get_request_by_id", return_value=None)
    mock_db = AsyncMock()
    request_id = uuid4()
    with pytest.raises(HTTPException) as exc_info:
        await get_request_by_id_service(request_id, mock_db)

    mock_get.assert_called_once_with(request_id, mock_db)
    assert exc_info.value.status_code == 404
