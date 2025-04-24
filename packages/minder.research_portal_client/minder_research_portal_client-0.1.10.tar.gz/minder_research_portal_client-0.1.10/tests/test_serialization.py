import json
import aiohttp
from minder.research_portal_client import Configuration, ApiClient
import minder.research_portal_client.models as models
from tests import async_test
import unittest.mock as mock


@async_test
async def test_deserialize_organizations():
    org_list = models.OrganizationsResponse([models._Organization("abc123", "Test-Org")])
    org_json = json.loads(json.dumps(org_list.to_dict()))

    config = Configuration(access_token="test-token")

    async def mockJson():
        return org_json

    mockResponse = mock.Mock(aiohttp.ClientResponse)
    mockResponse.json = mockJson

    async with ApiClient(config) as client:
        response = await client.deserialize(mockResponse, models.OrganizationsResponse)
        assert response == org_list


@async_test
async def test_deserialize_dataset_filter():
    filter = models.DatasetSourceFilter(["test_rel_dataset1", "test_rel_dataset2"])

    jd = json.dumps(filter.to_dict())
    filter_json = json.loads(jd)

    config = Configuration(access_token="test-token")

    async def mockJson():
        return filter_json

    mockResponse = mock.Mock(aiohttp.ClientResponse)
    mockResponse.json = mockJson

    async with ApiClient(config) as client:
        response = await client.deserialize(mockResponse, models.DatasetFilter)
        assert response == filter


@async_test
async def test_deserialize_available_datasets():
    datasets = models.AvailableDatasetsResponse(
        models._Parameters(["testCol1", "testCol2"]),
        {
            "test_category": {
                "test_dataset": models._DatasetDefinition(
                    ["testCol1", "testCol2", "testCol3"],
                    models.DatasetSourceFilter(["test_rel_dataset1", "test_rel_dataset2"]),
                )
            }
        },
    )

    jd = json.dumps(datasets.to_dict())
    datasets_json = json.loads(jd)

    config = Configuration(access_token="test-token")

    async def mockJson():
        return datasets_json

    mockResponse = mock.Mock(aiohttp.ClientResponse)
    mockResponse.json = mockJson

    async with ApiClient(config) as client:
        response = await client.deserialize(mockResponse, models.AvailableDatasetsResponse)
        assert response == datasets
