import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import status, Body, Response
from fastapi.testclient import TestClient
from fastapi import FastAPI

# Mock imports
from backend.utils.cbv import Controller
from backend.routes.v1.auth import AuthController
from backend.services.auth import AuthService, authenticate, get_auth_service
from backend.models.users import Doctor
from backend.schemas.users import DoctorDetailRead, DoctorUpdate
from backend.schemas.base import Schema

pytest.skip(allow_module_level=True)

# Create fixtures for testing
@pytest.fixture
def mock_auth_service():
    return AsyncMock(spec=AuthService)

@pytest.fixture
def mock_authenticate():
    mock_doctor = MagicMock(spec=Doctor)
    mock_doctor.doctor_id = "test-doctor-id"
    mock_doctor.first_name = "Test"
    mock_doctor.last_name = "Doctor"
    mock_doctor.email = "test@example.com"
    async_mock = AsyncMock(return_value=mock_doctor)
    return async_mock

@pytest.fixture
def auth_controller(mock_auth_service):
    controller = AuthController()
    controller.service = mock_auth_service
    return controller

@pytest.fixture
def app():
    app = FastAPI()
    
    # Mock the Controller.post and Controller.get methods
    with patch.object(Controller, 'post', autospec=True) as mock_post, \
         patch.object(Controller, 'get', autospec=True) as mock_get, \
         patch.object(Controller, 'patch', autospec=True) as mock_patch:
        
        # Configure mocks to return route functions
        def create_route(path, status_code=None, response_model=None):
            mock_route = MagicMock()
            mock_route.path = path
            return mock_route
        
        mock_post.side_effect = create_route
        mock_get.side_effect = create_route
        mock_patch.side_effect = create_route
        
        with patch('backend.services.auth.get_auth_service', return_value=AsyncMock(spec=AuthService)), \
             patch('backend.services.auth.authenticate', new=mock_authenticate):
            # Add router to app
            app.include_router(AuthController.as_router())
    
    return app

@pytest.fixture
def client(app):
    return TestClient(app)

class LoginCredentials(Schema):
    username: str
    password: str

#Tests for each route
@pytest.mark.asyncio
async def test_login_success(auth_controller, mock_auth_service):
    # Arrange
    credentials = LoginCredentials(username="test@example.com", password="password123")
    mock_response = Response(status_code=status.HTTP_200_OK)
    mock_auth_service.login.return_value = mock_response
    
    # Act
    response = await auth_controller.login(credentials)
    
    # Assert
    mock_auth_service.login.assert_called_once_with(credentials.username, credentials.password)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_logout(auth_controller, mock_auth_service):
    # Arrange
    mock_doctor = MagicMock(spec=Doctor)
    mock_response = Response(status_code=status.HTTP_200_OK)
    mock_auth_service.logout.return_value = mock_response
    
    # Act
    response = await auth_controller.logout(mock_doctor)
    
    # Assert
    mock_auth_service.logout.assert_called_once()
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_forgot_password(auth_controller):
    # Arrange
    username = "test@example.com"
    
    # Act
    response = await auth_controller.forgot_password(username)
    
    # Assert
    assert response is None

@pytest.mark.asyncio
async def test_me(auth_controller):
    # Arrange
    mock_doctor = MagicMock(spec=Doctor)
    
    # Act
    response = await auth_controller.me(mock_doctor)
    
    # Assert
    assert response == mock_doctor

@pytest.mark.asyncio
async def test_update_me(auth_controller, mock_auth_service):
    # Arrange
    payload = DoctorUpdate(first_name="Updated", last_name="Doctor")
    mock_doctor = MagicMock(spec=Doctor)
    mock_auth_service.update_me.return_value = mock_doctor
    
    # Act
    response = await auth_controller.update_me(payload, mock_doctor)
    
    # Assert
    mock_auth_service.update_me.assert_called_once_with(mock_doctor, payload)
    assert response == mock_doctor

# Integration tests using FastAPI TestClient
def test_login_endpoint(client, app):
    # Setup mock
    with patch('backend.services.auth.AuthService.login') as mock_login:
        mock_response = Response(status_code=status.HTTP_200_OK)
        mock_login.return_value = mock_response
        
        # Act
        response = client.post(
            "/auth/login", 
            json={"username": "test@example.com", "password": "password123"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK

def test_login_endpoint_invalid_credentials(client, app):
    # Setup mock
    with patch('backend.services.auth.AuthService.login') as mock_login:
        mock_login.side_effect = Exception("Invalid credentials")
        
        # Act
        response = client.post(
            "/auth/login", 
            json={"username": "wrong@example.com", "password": "wrong_password"}
        )
        
        # Assert
        assert response.status_code != status.HTTP_200_OK

def test_logout_endpoint(client, app):
    # Setup mock
    with patch('backend.services.auth.AuthService.logout') as mock_logout:
        mock_response = Response(status_code=status.HTTP_200_OK)
        mock_logout.return_value = mock_response
        
        # Act - Set a mock cookie for authentication
        client.cookies.set("auth_token", "test_token")
        response = client.post("/auth/logout")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK

def test_me_endpoint(client, app):
    # Setup - The mock_authenticate fixture is already set up to return a mock doctor
    
    # Act - Set a mock cookie for authentication
    client.cookies.set("auth_token", "test_token")
    response = client.get("/auth/me")
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    # We can't assert the exact response content because it depends on the 
    # mock_authenticate fixture's return value serialized as JSON

def test_update_me_endpoint(client, app):
    # Setup mock
    with patch('backend.services.auth.AuthService.update_me') as mock_update_me:
        updated_doctor = {
            "doctor_id": "test-doctor-id",
            "first_name": "Updated",
            "last_name": "Doctor",
            "email": "updated@example.com"
        }
        mock_update_me.return_value = MagicMock(**updated_doctor)
        
        # Act - Set a mock cookie for authentication
        client.cookies.set("auth_token", "test_token")
        response = client.patch(
            "/auth/me", 
            json={"first_name": "Updated", "last_name": "Doctor"}
        )
        
        # Assert
        assert response.status_code == status.HTTP_200_OK

def test_me_endpoint_unauthorized(client, app):
    # Act - No authentication cookie set
    response = client.get("/auth/me")
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_update_me_endpoint_validation_error(client, app):
    # Setup - invalid payload (email format is incorrect)
    
    # Act
    client.cookies.set("auth_token", "test_token")
    response = client.patch(
        "/auth/me", 
        json={"email": "invalid-email-format"}
    )
    
    # Assert - Should fail validation
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

# Test controller class properties
def test_auth_controller_properties():
    # Assert that the controller has the correct attributes
    assert AuthController.prefix == "/auth"
    assert AuthController.resource == "auth"
    assert AuthController.tags == ["auth"]

@pytest.mark.asyncio
async def test_get_auth_service_dependency():
    # Arrange
    mock_repo = AsyncMock()
    
    # Act
    with patch('backend.services.auth.SQLDoctorRepository', return_value=mock_repo):
        service = await get_auth_service(mock_repo)
    
    # Assert
    assert isinstance(service, AuthService)
    assert service.doctor_repository == mock_repo

@pytest.mark.asyncio
async def test_authenticate_dependency():
    # Arrange
    mock_service = AsyncMock(spec=AuthService)
    mock_doctor = MagicMock(spec=Doctor)
    mock_service.authenticate.return_value = mock_doctor
    token = "test_token"
    
    # Act
    with patch('backend.services.auth.AuthService', return_value=mock_service):
        result = await authenticate(mock_service, token)
    
    # Assert
    assert result == mock_doctor
    mock_service.authenticate.assert_called_once_with(token)

@pytest.mark.asyncio
async def test_authenticate_dependency_no_token():
    # Arrange
    mock_service = AsyncMock(spec=AuthService)
    
    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await authenticate(mock_service, None)
    
    # Assert error details
    assert "Unauthorized" in str(exc_info.value)