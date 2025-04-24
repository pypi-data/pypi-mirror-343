import pytest
from minder.research_portal_client import Configuration


class TestConfiguration(object):
    @pytest.fixture(autouse=True)
    def reset_default_config(self):
        Configuration._default = None
        yield
        Configuration._default = None

    def test_set_default(self):
        # Arrange
        default_config = Configuration(
            base_url="https://test/api",
            access_token="test-token",
        )
        Configuration.set_default(default_config)

        # Act
        config = Configuration()

        # Assert
        assert config.__dict__ == default_config.__dict__
