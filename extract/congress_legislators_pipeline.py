import dlt
from dlt.sources.rest_api import (
    RESTAPIConfig,
    rest_api_resources,
)


@dlt.source(name="congress_legislators")
def congress_legislators_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://unitedstates.github.io/congress-legislators/",
        },
        "resource_defaults": {
            "primary_key": "id__bioguide",
            "write_disposition": "merge",
        },
        "resources": [
            {
                "name": "legislators-current",
                "endpoint": {
                    "path": "legislators-current.json",
                    "method": "GET",
                    "paginator": "single_page",
                },
            },
        ],
    }

    yield from rest_api_resources(config)


def load_congress_legislators() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="congress_legislators",
        destination="duckdb",
        dataset_name="legislators_current",
        progress="log",
    )

    load_info = pipeline.run(congress_legislators_source())
    print(load_info)


if __name__ == "__main__":
    load_congress_legislators()
