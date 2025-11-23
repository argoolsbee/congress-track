import time

import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig
from geopy.geocoders import Nominatim


@dlt.source(name="congress_legislators")
def congress_legislators_source():
    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://unitedstates.github.io/congress-legislators/",
        },
        "resource_defaults": {
            "endpoint": {
                "method": "GET",
                "paginator": "single_page",
            },
            "write_disposition": "merge",
        },
        "resources": [
            {
                "name": "legislators-current",
                "endpoint": {
                    "path": "legislators-current.json",
                },
                "primary_key": "id__bioguide",
            },
            {
                "name": "legislators-historical",
                "endpoint": {
                    "path": "legislators-historical.json",
                },
                "primary_key": "id__bioguide",
            },
            {
                "name": "legislators-district-offices",
                "endpoint": {
                    "path": "legislators-district-offices.json",
                },
                "primary_key": "id__bioguide",
            },
            {
                "name": "legislators-social-media",
                "endpoint": {
                    "path": "legislators-social-media.json",
                },
                "primary_key": "id__bioguide",
            },
        ],
    }

    yield from rest_api_resources(config)


def geocode_missing_coordinates(pipeline) -> None:
    """Geocode missing latitude/longitude using Nominatim."""
    geolocator = Nominatim(user_agent="congress_legislators_pipeline")

    with pipeline.sql_client() as conn:
        # Initialize geocoded column if it doesn't exist
        try:
            alter_query = """
            ALTER TABLE legislators_district_offices__offices
            ADD COLUMN geocoded BOOLEAN DEFAULT FALSE
            """
            conn.execute_query(alter_query)
        except Exception:
            # Column might already exist, which is fine
            pass

        # Fetch records with missing coordinates
        query_missing = """
        SELECT address, city, state, zip
        FROM legislators_district_offices__offices
        WHERE latitude IS NULL OR longitude IS NULL
        """

        with conn.execute_query(query_missing) as result:
            missing_records = result.fetchall()

        if not missing_records:
            print("No missing coordinates to geocode.")
            return

        print(f"\nGeocoding {len(missing_records)} records with missing coordinates...")
        geocoded_count = 0
        failed_count = 0

        for address, city, state, zip_code in missing_records:
            # Build full address
            address_parts = [address, city, state, zip_code]
            full_address = ", ".join(str(p) for p in address_parts if p)

            try:
                # Geocode the full address first
                location = geolocator.geocode(full_address)

                # Fallback: try geocoding with just city, state, zip if full address fails
                if not location:
                    fallback_address = ", ".join(str(p) for p in [city, state, zip_code] if p)
                    location = geolocator.geocode(fallback_address)

                if location:
                    lat, lon = location.latitude, location.longitude  # pyright: ignore[reportAttributeAccessIssue]

                    # Escape single quotes for SQL and format lat/lon as strings
                    address_escaped = address.replace("'", "''") if address else ""
                    city_escaped = city.replace("'", "''") if city else ""
                    state_escaped = state.replace("'", "''") if state else ""
                    lat_str = f"{lat:.6f}"
                    lon_str = f"{lon:.6f}"

                    # Update the database with coordinates and mark as geocoded
                    update_query = f"""
                    UPDATE legislators_district_offices__offices
                    SET latitude = {lat_str}, longitude = {lon_str}, geocoded = TRUE
                    WHERE address = '{address_escaped}' 
                    AND city = '{city_escaped}' 
                    AND state = '{state_escaped}'
                    """

                    conn.execute_query(update_query)

                    geocoded_count += 1
                    print(f"✓ {full_address}: ({lat}, {lon})")
                else:
                    failed_count += 1
                    print(f"✗ {full_address}: No location found")

                # Rate limit: Nominatim requests 1 per second
                time.sleep(1)

            except Exception as e:
                failed_count += 1
                print(f"✗ {full_address}: Error - {e}")
                time.sleep(1)

        print(f"\nGeocoding complete: {geocoded_count} successful, {failed_count} failed")


def load_congress_legislators() -> None:
    pipeline = dlt.pipeline(
        pipeline_name="congress_legislators",
        destination=dlt.destinations.duckdb(destination_name="congress_track"),
        dataset_name="congress_legislators",
        progress="log",
    )

    load_info = pipeline.run(congress_legislators_source())
    print(load_info)

    # Geocode missing coordinates
    geocode_missing_coordinates(pipeline)


if __name__ == "__main__":
    load_congress_legislators()
