import pytest
import redis
from app.utils.redis_utils import get_redis_client
from app.core.config import settings

@pytest.mark.integration
@pytest.mark.skipif(not pytest.config.getoption("--run-integration"),
                    reason="Needs Redis server running")
def test_real_redis_connection():
    """Test actual Redis connection with container"""
    client = None
    try:
        client = get_redis_client()
        # Test basic operations
        test_key = "test:integration"
        client.set(test_key, "success")
        assert client.get(test_key) == "success"
    finally:
        if client:
            client.delete(test_key)