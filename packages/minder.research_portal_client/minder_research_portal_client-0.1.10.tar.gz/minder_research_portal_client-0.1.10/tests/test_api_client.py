from minder.research_portal_client import Configuration, ApiClient
from tests import async_test


@async_test
async def test_create_api_client():
    config = Configuration(
        base_url="https://test/api",
        access_token="test-token",
    )
    async with ApiClient(configuration=config) as client:
        assert client.info is not None
        assert client.export is not None
        assert client.download is not None
        assert client.reports is not None
