import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import redis
from app.main import app
from app.core.config import settings

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_redis():
    with patch('app.utils.redis_utils.get_redis_client') as mock:
        mock_redis = MagicMock(spec=redis.Redis)
        mock.return_value = mock_redis
        yield mock_redis

@pytest.fixture
def mock_selenium():
    with patch('selenium.webdriver.Remote') as mock:
        mock_driver = MagicMock()
        mock.return_value = mock_driver
        yield mock_driver

@pytest.fixture
def real_redis_client():
    """Fixture for integration tests with real Redis"""
    client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        decode_responses=True
    )
    yield client
    # Cleanup
    for key in client.scan_iter("test:*"):
        client.delete(key)