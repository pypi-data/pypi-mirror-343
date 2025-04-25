import pytest
from unittest.mock import AsyncMock, patch
from utils.MessagingUtil import MessagingUtil

@pytest.mark.asyncio
async def test_getClient():
    host_address = "nats://localhost:4222"
    messaging_util = MessagingUtil(host_address)

    with patch("nats.connect", new_callable=AsyncMock) as mock_connect:
        mock_client = AsyncMock()
        mock_connect.return_value = mock_client

        client = await messaging_util.getClient()

        mock_connect.assert_called_once_with(host_address)
        assert client == mock_client

@pytest.mark.asyncio
async def test_publish():
    host_address = "nats://localhost:4222"