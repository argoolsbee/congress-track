import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source(name="congress_gov_api")
def congress_gov_api_source(congress_api_key: str = dlt.secrets["congress_api_key"]):
    """Source from Congress.gov API v3 endpoint.
    Requires congress_api_key to be set in secrets.toml.
    """
    if not congress_api_key:
        raise ValueError(
            "congress_api_key not found in .dlt/secrets.toml."
            "Get your API key at https://api.congress.gov/ and add it to .dlt/secrets.toml"
        )

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://api.congress.gov/v3/",
            "auth": {
                "type": "api_key",
                "name": "api_key",
                "api_key": congress_api_key,
                "location": "query",
            },  # type: ignore
        },
        "resource_defaults": {
            "endpoint": {
                "method": "GET",
                "paginator": {
                    "type": "json_link",
                    "next_url_path": "pagination.next",
                },
                "data_selector": "members",
                "params": {
                    "fromDateTime": "{incremental.start_value}",
                    "limit": 250,
                },
                "incremental": {
                    "cursor_path": "updateDate",
                    "initial_value": "1700-01-01T00:00:00Z",
                },
            },
            "write_disposition": "merge",
        },
        "resources": [
            {
                "name": "members",
                "endpoint": {
                    "path": "member",
                },
                "primary_key": "bioguideId",
            },
        ],
    }

    yield from rest_api_resources(config)


def load_congress_gov_api() -> None:
    """Load data from Congress.gov API into DuckDB."""
    pipeline = dlt.pipeline(
        pipeline_name="congress_gov_api",
        destination=dlt.destinations.duckdb(destination_name="congress_track"),
        dataset_name="congress_gov",
        progress="log",
    )

    load_info = pipeline.run(congress_gov_api_source())
    print(load_info)


if __name__ == "__main__":
    load_congress_gov_api()
