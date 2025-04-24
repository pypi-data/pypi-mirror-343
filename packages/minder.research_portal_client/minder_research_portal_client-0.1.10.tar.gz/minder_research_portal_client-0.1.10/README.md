# Research Portal Client

Library to interact with Minder Research APIs.

## Example

```bash
pip install minder.research-portal-client
```

```python
import logging
import asyncio
import datetime
import sys
from minder.research_portal_client import Configuration, JobManager
from minder.research_portal_client.models import (
    ExportJobRequest,
    ExportJobRequestDataset,
)


logging.basicConfig(level=logging.INFO)

Configuration.set_default(
    Configuration(
        access_token="---REDACTED---",
    )
)


async def example1():
    async with JobManager() as job_manager:
        now = datetime.datetime.today()
        since = now - datetime.timedelta(days=7)
        datasets: dict(str, ExportJobRequestDataset) = {
            "patients": ExportJobRequestDataset(),
            "observation_notes": ExportJobRequestDataset(),
        }

        export_job = ExportJobRequest(since, datasets=datasets)
        job_id = await job_manager.submit(export_job)
        job = await job_manager.wait(job_id)
        files = await job_manager.download(job)
        print(files)


async def example2():
    job_id = "c25249e0-82ff-43d1-9676-f3cead0228b9"
    async with JobManager() as job_manager:
        files = await job_manager.download(job_id)
        print(files)


async def example3():
    async with JobManager() as job_manager:
        datasets = await job_manager.client.info.list_datasets()
        print(datasets)

        organizations = await job_manager.client.info.list_organizations()
        print(organizations)

        reports = await job_manager.client.reports.list_reports()
        print(reports)


async def main():
    await example1()
    await example2()
    await example3()


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
```

## Development

### Setup

```bash
uv sync
```

### Run tests
  
```bash
uv run pytest
```

### Code Coverage

This command consists of 2 parts:

- running tests with coverage collection
- formatting the report: `report` (text to stdout), `xml` (GitLab compatible: cobertura), `html` (visual)

```bash
uv run coverage run -m pytest && uv run coverage report -m
```

### Linting

```bash
uv run flake8
```

### Formatting

```bash
uv run black .
```

### Type Checking

```bash
uv run mypy .
```

### Publishing

```bash
uv publish --token pypi-…
```
