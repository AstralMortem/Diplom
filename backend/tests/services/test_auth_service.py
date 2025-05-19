import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid
from datetime import datetime, timedelta, UTC
import jwt
from fastapi import Response, Depends
from fastapi.security import APIKeyCookie
from http.cookies import SimpleCookie

# Import the necessary classes and functions
from backend.core import MedServiceException, status
from backend.models.users import Doctor
from backend.schemas.users import DoctorUpdate
from backend.utils.password_helper import PasswordHelperProtocol
from backend.repositories.doctors import IDoctorRepository
from backend.services.auth import AuthService, authenticate, get_auth_service
from backend.config import config

# Create test fixtures
@pytest.fixture
def mock_doctor_repository():
    return AsyncMock(spec=IDoctorRepository)

@pytest.fixture
def mock_password_helper():
    password_helper = MagicMock(spec=PasswordHelperProtocol)
    # Set up default behavior
    password_helper.hash.return_value = "hashed_password"
    password_helper.verify_and_update.return_value = (True, None)
    return password_helper

@pytest.fixture
def auth_service(mock_doctor_repository, mock_password_helper):
    service = AuthService(mock_doctor_repository)
    service.password_helper = mock_password_helper
    return service

@pytest.fixture
def mock_doctor():
    return MagicMock(
        spec=Doctor,
        doctor_id=uuid.uuid4(),
        email="doctor@example.com",
        phone_number="1234567890",
        hashed_password="hashed_password",
        is_active=True,
    )

@pytest.fixture
def mock_token():
    return "mock_jwt_token"

# Test the AuthService class methods
@pytest.mark.asyncio
async def test_login_successful(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    username = "doctor@example.com"
    password = "password123"
    mock_doctor_repository.get_doctor_for_login.return_value = mock_doctor
    
    # Setup mock for _create_login_response
    with patch.object(auth_service, '_create_login_response') as mock_create_response:
        mock_response = Response(status_code=status.HTTP_204_NO_CONTENT)
        mock_create_response.return_value = mock_response
        
        # Act
        response = await auth_service.login(username, password)
        
        # Assert
        mock_doctor_repository.get_doctor_for_login.assert_called_once_with(username)
        auth_service.password_helper.verify_and_update.assert_called_once_with(
            password, mock_doctor.hashed_password
        )
        mock_create_response.assert_called_once_with(mock_doctor)
        assert response == mock_response

@pytest.mark.asyncio
async def test_login_invalid_credentials(auth_service, mock_doctor_repository):
    # Arrange
    username = "nonexistent@example.com"
    password = "wrong_password"
    mock_doctor_repository.get_doctor_for_login.return_value = None
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await auth_service.login(username, password)
    
    assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in exc_info.value.title

@pytest.mark.asyncio
async def test_login_inactive_user(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    username = "inactive@example.com"
    password = "password123"
    mock_doctor.is_active = False
    mock_doctor_repository.get_doctor_for_login.return_value = mock_doctor
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await auth_service.login(username, password)
    
    assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in exc_info.value.title

@pytest.mark.asyncio
async def test_login_invalid_password(auth_service, mock_doctor_repository, mock_doctor, mock_password_helper):
    # Arrange
    username = "doctor@example.com"
    password = "wrong_password"
    mock_doctor_repository.get_doctor_for_login.return_value = mock_doctor
    auth_service.password_helper.verify_and_update.return_value = (False, None)
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await auth_service.login(username, password)
    
    assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
    assert "Invalid credentials" in exc_info.value.title

@pytest.mark.asyncio
async def test_login_password_update(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    username = "doctor@example.com"
    password = "password123"
    new_hash = "new_hashed_password"
    mock_doctor_repository.get_doctor_for_login.return_value = mock_doctor
    auth_service.password_helper.verify_and_update.return_value = (True, new_hash)
    
    # Setup mock for test
    with patch.object(auth_service, '_create_login_response') as mock_create_response:
        mock_response = Response(status_code=status.HTTP_204_NO_CONTENT)
        mock_create_response.return_value = mock_response
        
        # Act
        await auth_service.login(username, password)
        
        # Assert
        mock_doctor_repository.update.assert_called_once_with(
            mock_doctor, {"hashed_password": new_hash}
        )

@pytest.mark.asyncio
async def test_logout(auth_service):
    # Act
    response = await auth_service.logout()
    
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert any(cookie[0] == config.AUTH_COOKIE_NAME for cookie in response.raw_headers)

@pytest.mark.asyncio
async def test_update_me_safe(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    payload = DoctorUpdate(
        first_name="Updated",
        last_name="Doctor",
        email="updated@example.com",
        phone_number="9876543210",
        role_id=1,  # This should be ignored in safe mode
        department_id=1,  # This should be ignored in safe mode
    )
    
    # Set up repository mocks
    mock_doctor_repository.get_by_email.return_value = None
    mock_doctor_repository.get_by_phone_number.return_value = None
    mock_doctor_repository.update.return_value = mock_doctor
    
    # Act
    result = await auth_service.update_me(mock_doctor, payload)
    
    # Assert
    mock_doctor_repository.get_by_email.assert_called_once_with(payload.email)
    mock_doctor_repository.get_by_phone_number.assert_called_once_with(payload.phone_number)
    
    # Check that role_id and department_id were excluded
    update_call_args = mock_doctor_repository.update.call_args[0][1]
    assert "role_id" not in update_call_args
    assert "department_id" not in update_call_args
    
    assert result == mock_doctor

@pytest.mark.asyncio
async def test_update_me_unsafe(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    role_id = 1
    department_id = 1
    payload = DoctorUpdate(
        first_name="Updated",
        last_name="Doctor",
        role_id=role_id,
        department_id=department_id,
    )
    
    # Set up repository mocks
    mock_doctor_repository.update.return_value = mock_doctor
    
    # Act
    result = await auth_service.update_me(mock_doctor, payload, safe=False)
    
    # Assert
    update_call_args = mock_doctor_repository.update.call_args[0][1]
    assert update_call_args.get("role_id") == role_id
    assert update_call_args.get("department_id") == department_id
    assert result == mock_doctor

@pytest.mark.asyncio
async def test_update_me_with_password(auth_service, mock_doctor_repository, mock_doctor, mock_password_helper):
    # Arrange
    new_password = "new_password123"
    payload = DoctorUpdate(password=new_password)
    
    # Set up repository mocks
    mock_doctor_repository.update.return_value = mock_doctor
    
    # Act
    result = await auth_service.update_me(mock_doctor, payload)
    
    # Assert
    mock_password_helper.hash.assert_called_once_with(new_password)
    update_call_args = mock_doctor_repository.update.call_args[0][1]
    assert "hashed_password" in update_call_args
    assert update_call_args["hashed_password"] == "hashed_password"  # From the mock
    assert result == mock_doctor

@pytest.mark.asyncio
async def test_update_me_email_exists(auth_service, mock_doctor_repository):
    # Arrange
    existing_email = "existing@example.com"
    payload = DoctorUpdate(email=existing_email)
    mock_doctor = MagicMock(spec=Doctor)
    
    # Set up repository mocks to simulate email already existing
    mock_doctor_repository.get_by_email.return_value = MagicMock()
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await auth_service.update_me(mock_doctor, payload)
    
    assert exc_info.value.code == status.HTTP_400_BAD_REQUEST
    assert "Email already exists" in exc_info.value.title

@pytest.mark.asyncio
async def test_update_me_phone_exists(auth_service, mock_doctor_repository):
    # Arrange
    existing_phone = "9876543210"
    payload = DoctorUpdate(phone_number=existing_phone)
    mock_doctor = MagicMock(spec=Doctor)
    
    # Set up repository mocks
    mock_doctor_repository.get_by_email.return_value = None
    mock_doctor_repository.get_by_phone_number.return_value = MagicMock()
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await auth_service.update_me(mock_doctor, payload)
    
    assert exc_info.value.code == status.HTTP_400_BAD_REQUEST
    assert "Phone number already exists" in exc_info.value.title

@pytest.mark.asyncio
async def test_authenticate_valid_token(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    token = "valid_token"
    doctor_id = str(mock_doctor.doctor_id)
    
    # Mock the _decode_auth_token method
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.return_value = {"sub": doctor_id}
        mock_doctor_repository.get_by_id.return_value = mock_doctor
        
        # Act
        result = await auth_service.authenticate(token)
        
        # Assert
        mock_decode.assert_called_once_with(token)
        mock_doctor_repository.get_by_id.assert_called_once_with(mock_doctor.doctor_id)
        assert result == mock_doctor

@pytest.mark.asyncio
async def test_authenticate_invalid_token_format(auth_service):
    # Arrange
    token = "invalid_token"
    
    # Mock the _decode_auth_token method to raise an exception
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.side_effect = MedServiceException(
            status.HTTP_401_UNAUTHORIZED, "Invalid token", "Invalid token"
        )
        
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            await auth_service.authenticate(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

@pytest.mark.asyncio
async def test_authenticate_missing_sub_claim(auth_service):
    # Arrange
    token = "missing_sub_token"
    
    # Mock the _decode_auth_token method
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.return_value = {}  # Missing 'sub' claim
        
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            await auth_service.authenticate(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

@pytest.mark.asyncio
async def test_authenticate_invalid_uuid(auth_service):
    # Arrange
    token = "invalid_uuid_token"
    
    # Mock the _decode_auth_token method
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.return_value = {"sub": "not-a-uuid"}
        
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            await auth_service.authenticate(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

@pytest.mark.asyncio
async def test_authenticate_doctor_not_found(auth_service, mock_doctor_repository):
    # Arrange
    doctor_id = uuid.uuid4()
    token = "doctor_not_found_token"
    
    # Mock the _decode_auth_token method
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.return_value = {"sub": str(doctor_id)}
        mock_doctor_repository.get_by_id.return_value = None
        
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            await auth_service.authenticate(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

@pytest.mark.asyncio
async def test_authenticate_inactive_doctor(auth_service, mock_doctor_repository, mock_doctor):
    # Arrange
    token = "inactive_doctor_token"
    doctor_id = str(mock_doctor.doctor_id)
    mock_doctor.is_active = False
    
    # Mock the _decode_auth_token method
    with patch.object(auth_service, '_decode_auth_token') as mock_decode:
        mock_decode.return_value = {"sub": doctor_id}
        mock_doctor_repository.get_by_id.return_value = mock_doctor
        
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            await auth_service.authenticate(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

def test_generate_auth_token(auth_service, mock_doctor):
    # Arrange
    with patch('jwt.encode') as mock_encode:
        mock_encode.return_value = "jwt_token"
        
        # Act
        token = auth_service._generate_auth_token(mock_doctor)
        
        # Assert
        assert token == "jwt_token"
        mock_encode.assert_called_once()
        
        # Verify payload contains the correct claims
        call_args = mock_encode.call_args[0]
        payload = call_args[0]
        assert payload["sub"] == str(mock_doctor.doctor_id)
        assert "exp" in payload
        assert "iat" in payload
        assert payload["aud"] == config.JWT_AUTH_AUDIENCE

def test_decode_auth_token_valid(auth_service):
    # Arrange
    token = "valid_token"
    decoded = {"sub": "user_id", "exp": datetime.now(UTC) + timedelta(days=1)}
    
    with patch('jwt.decode', return_value=decoded) as mock_decode:
        # Act
        result = auth_service._decode_auth_token(token)
        
        # Assert
        assert result == decoded
        mock_decode.assert_called_once_with(
            token,
            config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM],
            audience=config.JWT_AUTH_AUDIENCE,
        )

def test_decode_auth_token_invalid(auth_service):
    # Arrange
    token = "invalid_token"
    
    with patch('jwt.decode', side_effect=jwt.PyJWTError("Invalid token")) as mock_decode:
        # Act & Assert
        with pytest.raises(MedServiceException) as exc_info:
            auth_service._decode_auth_token(token)
        
        assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid token" in exc_info.value.title

def test_create_login_response(auth_service, mock_doctor):
    # Arrange
    token = "test_token"
    
    with patch.object(auth_service, '_generate_auth_token', return_value=token) as mock_generate:
        # Act
        response = auth_service._create_login_response(mock_doctor)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        mock_generate.assert_called_once_with(mock_doctor)
        
        cookie_found = False
        for cookie in [SimpleCookie(j.decode()) for _, j in response.raw_headers]:
            print(cookie)
            try:
                value = cookie.get(config.AUTH_COOKIE_NAME, None)
                if value is None:
                    continue
                assert token == value.__dict__["_value"]
            except ValueError:
                assert False


# Test the utility functions
@pytest.mark.asyncio
async def test_get_auth_service():
    # Arrange
    mock_repo = AsyncMock()
    
    # Act
    service = await get_auth_service(mock_repo)
    
    # Assert
    assert isinstance(service, AuthService)
    assert service.doctor_repository == mock_repo

@pytest.mark.asyncio
async def test_authenticate_middleware_no_token():
    # Arrange
    auth_service_mock = AsyncMock()
    
    # Act & Assert
    with pytest.raises(MedServiceException) as exc_info:
        await authenticate(auth_service_mock, None)
    
    assert exc_info.value.code == status.HTTP_401_UNAUTHORIZED
    assert "Auth Token not set" in exc_info.value.description

@pytest.mark.asyncio
async def test_authenticate_middleware_valid_token():
    # Arrange
    token = "valid_auth_token"
    mock_doctor = MagicMock()
    auth_service_mock = AsyncMock()
    auth_service_mock.authenticate.return_value = mock_doctor
    
    # Act
    result = await authenticate(auth_service_mock, token)
    
    # Assert
    auth_service_mock.authenticate.assert_called_once_with(token)
    assert result == mock_doctor